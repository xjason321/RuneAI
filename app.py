from flask import Flask, render_template, request
import tensorflow as tf
import numpy as np
import json

def invert_and_rotate(array):
    # Clockwise rotation
    rotated_array = [[array[j][i] for j in range(len(array))] for i in range(len(array[0]))]

    return rotated_array

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    grid = [['#ffffff'] * 28 for _ in range(28)]  # Initial grid with white pixels
    return render_template('index.html', grid=grid)

@app.route('/', methods=['POST'])
def update_grid():
    grid = [[0] * 28 for _ in range(28)]  # Initialize grid with white pixels

    canvas_data = json.loads(request.form.get('canvasData'))
    canvas = canvas_data['canvas']

    for row in range(28):
        for col in range(28):
            pixel_color = canvas[row][col]
            if pixel_color:
                grid[row][col] = int(pixel_color/255)
    
    grid = invert_and_rotate(grid)

    model = tf.keras.models.load_model('handwritten.model')

    user_array = np.array(grid)

    # Reshape the array
    reshaped_array = user_array.reshape((1, 28, 28))

    # Make predictions and sort
    predictions = model.predict(reshaped_array)
    sorted_predictions = sorted(enumerate(predictions[0]), key=lambda x: x[1], reverse=True)

    mapping = {
        1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E', 6: 'F', 7: 'G', 8: 'H',
        9: 'I', 10: 'J', 11: 'K', 12: 'L', 13: 'M', 14: 'N', 15: 'O', 16: 'P',
        17: 'Q', 18: 'R', 19: 'S', 20: 'T', 21: 'U', 22: 'V',23: 'W', 24: 'X', 25: 'Y', 26: 'Z',
        27: 'a', 28: 'b', 29: 'c', 30: 'd', 31: 'e', 32: 'f', 33: 'g', 34: 'h', 35: 'i',
        36: 'j', 37: 'Unknown'
    }
    
    index1, likelihood1 = sorted_predictions[0]
    index2, likelihood2 = sorted_predictions[1]
    index3, likelihood3 = sorted_predictions[2]
    index4, likelihood4 = sorted_predictions[3]
    index5, likelihood5 = sorted_predictions[4]

    m1 = f"Letter {mapping[index1]}: Likelihood {format(likelihood1 * 100, '.2f')}%" if likelihood1 > .10 else "The AI is struggling with this one. Try again!"
    m2 = f"Letter {mapping[index2]}: Likelihood {format(likelihood2 * 100, '.2f')}%" if likelihood2 > .05 else " "
    m3 = f"Letter {mapping[index3]}: Likelihood {format(likelihood3 * 100, '.2f')}%" if likelihood3 > .05 else " "
    m4 = f"Letter {mapping[index4]}: Likelihood {format(likelihood4 * 100, '.2f')}%" if likelihood4 > .05 else " "
    m5 = f"Letter {mapping[index5]}: Likelihood {format(likelihood5 * 100, '.2f')}%" if likelihood5 > .05 else " "

    return render_template('index.html', grid=grid, m1=m1, m2=m2, m3=m3, m4=m4, m5=m5)

if __name__ == '__main__':
    app.run()
