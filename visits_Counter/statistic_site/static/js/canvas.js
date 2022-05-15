const canvasPlot = document.getElementById('month_stat_plot');
const ctx = canvasPlot.getContext('2d');

const canvasPlotWidth = canvasPlot.clientWidth;
const canvasPlotHeight = canvasPlot.clientHeight;

const scaleX = 20;
const scaleY = 20;

const xAxis = 0;
const yAxis = Math.round(canvasPlotHeight/scaleY) * scaleY;

ctx.font = `${Math.round(scaleX/2)}px Arial`;
ctx.fontAlign = 'left';
ctx.textBaseline = 'top';


// Grid
ctx.beginPath();
ctx.strokeStyle = '#white';
ctx.lineWidth = 0.4;

for (let i = 0; i <= canvasPlotWidth; i = i + scaleX) {
    if (i % 300 == 0){
        ctx.moveTo(i, 0);
        ctx.lineTo(i, canvasPlotHeight);
    }
}

for (let i = 0; i <= canvasPlotHeight; i = i + scaleY) {
    if (i % 160 == 0){
        ctx.moveTo(0, i);
        ctx.lineTo(canvasPlotWidth, i);
    }
}

ctx.stroke();
ctx.closePath();


// Axis
ctx.beginPath();
ctx.strokeStyle = '#000000';
ctx.lineWidth = 1;
ctx.moveTo(xAxis,0);
ctx.lineTo(xAxis, canvasPlotHeight);

ctx.moveTo(0, yAxis);
ctx.lineTo(canvasPlotWidth, yAxis);

ctx.stroke();
ctx.closePath();

let chart = new Chart()