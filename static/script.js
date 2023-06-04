document.addEventListener('DOMContentLoaded', function() {
    const pixelGrid = document.getElementById('pixel-grid');
    let isDrawing = false;
    let previousPixel = null;

    pixelGrid.addEventListener('mousedown', function(event) {
        if (event.target.classList.contains('pixel')) {
            isDrawing = true;
            togglePixelColor(event.target);
            previousPixel = event.target;
        }
    });

    pixelGrid.addEventListener('mousemove', function(event) {
        if (isDrawing && event.target.classList.contains('pixel') && event.target !== previousPixel) {
            togglePixelColor(event.target);
            previousPixel = event.target;
        }
    });

    pixelGrid.addEventListener('mouseup', function() {
        isDrawing = false;
        previousPixel = null;
    });
});

function togglePixelColor(pixel) {
    pixel.style.backgroundColor = 'rgb(255, 255, 255)';
}

function clearPixels() {
    const pixels = document.getElementsByClassName('pixel');
    for (let i = 0; i < pixels.length; i++) {
        pixels[i].style.backgroundColor = '';
    }
}

function savePixels() {
    const pixels = document.getElementsByClassName('pixel');
    const canvas = [];

    for (let i = 0; i < pixels.length; i++) {
        const pixel = pixels[i];
        const pixelColor = pixel.style.backgroundColor;
        const rgb = pixelColor.substring(4, pixelColor.length - 1)
            .replace(/ /g, '')
            .split(',');

        const rValue = parseInt(rgb[0]);

        if (i % 28 === 0) {
            canvas.push([rValue]);
        } else {
            canvas[Math.floor(i / 28)].push(rValue);
        }
    }

    const form = document.createElement('form');
    form.method = 'POST';

    // Convert canvas data to JSON and create a hidden input field
    const canvasData = { 'canvas': canvas };
    const canvasInput = document.createElement('input');
    canvasInput.type = 'hidden';
    canvasInput.name = 'canvasData';
    canvasInput.value = JSON.stringify(canvasData);
    form.appendChild(canvasInput);

    document.body.appendChild(form);
    form.submit();
}
