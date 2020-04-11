document.addEventListener('DOMContentLoaded', () => {

  // Connect to websocket
  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  // When connected, configure buttons
  socket.on('connect', function(){

      // Each button should emit a "submit vote" event
      document.querySelector('#data_stream_control').onclick = function(){
              let action = this.value;
              socket.emit('start-stream', {'action': action});
              if(action == "start"){
                this.value = "stop";
                this.innerHTML = "Stop Stream";
              }
              else{
                this.value = "start";
                this.innerHTML = "Start Stream";
              }
          };
      });

   document.querySelector('#model-calibration').onclick = function(){
      let start_button = document.querySelector('#model-play');
      let test_button = document.querySelector('#model-test');
      if (this.value == "0"){
          this.value = "1";
          this.innerHTML = "Stop Calibration";
          start_button.hidden = false;
          test_button.hidden = false;
       }
       else{
          this.value = "0";
          this.innerHTML = "Start Calibration";
          start_button.hidden = true;
          test_button.hidden = true;
       }
   };


});