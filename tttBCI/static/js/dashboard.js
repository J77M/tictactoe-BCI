  document.addEventListener('DOMContentLoaded', () => {

      // Connect to websocket
      var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

      // When connected, configure buttons
      socket.on('connect', function(){

          // Each button should emit a "submit vote" event
          document.querySelector('#data_stream_control').onclick = function(){
                  let action = this.value
                  socket.emit('start-stream', {'action': action});
                  if(action == "start"){
                    this.value = "stop"
                    this.innerHTML = "Stop Stream"
                  }
                  else{
                    this.value = "start"
                    this.innerHTML = "Start Stream"
                  }
              };
          });

      // When a new vote is announced, add to the unordered list
      socket.on('return data', function(data){
        let traces = []
        x_data = data.time
        for (i = 0; i < data.data.length; i++) {
              var trace = {x: x_data, y: data.data[i], mode: 'lines', type: 'scatter'};
              traces.push(trace)
        }
        Plotly.newPlot('data-stream-graph', traces);
    })
  });