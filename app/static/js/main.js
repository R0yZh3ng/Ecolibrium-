window.onload = function() {
  timeAnimations();
};

/** Determines the timings of animating everything */
function timeAnimations() {
  drawChart();
  incrementUsers();
}

/** Uses the information in .line-chart ul li to create connecting lines */
function drawChart() {
  const data = document.querySelectorAll(".line-chart-data");
  dataMin = getComputedStyle(data[0]).getPropertyValue('--value'), dataMax = dataMin;
  const total = document.querySelectorAll(".line-chart-total")[0];
  const positions = document.querySelectorAll(".line-chart-lines");
  // Find min and max of data
  for (i=0; i<data.length; i++) {
    crnt = getComputedStyle(data[i]).getPropertyValue('--value');
    if (crnt < dataMin) {
      dataMin = crnt;
    } else if (crnt > dataMax) {
      dataMax = crnt;
    }
  }
  // Change chart data to display on graph
  for (i=0; i<data.length; i++) {
    crnt = data[i];
  }
}

function incrementUsers() {

}

function incrementTons() {

}

function animateChart() {

}