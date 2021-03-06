document.addEventListener('DOMContentLoaded', () => {

      /**
     * Runs animation cycle(flashing rows and columns)
     * @cycle_func -  function to be run every cycle
     * @end_func - function to be run every cycle finished
     * @events_per_cycle - number of flashing events in cycle
     * @cycles - number of cycles
     * @interval - interval between events in cycle (in ms)
     */
    function runAnimationCycle(cycle_func, end_func, events_per_cycle, cycles, interval){

        function startAnimation(cycle_func, end_func, events_per_cycle, cycles, interval){
            var animation_intervalId = null;
            var animation_counter = 0;

            var animate = function(){
                 if(document.querySelectorAll(".data-selected").length != 0){
                    document.querySelectorAll(".data-selected").forEach(function(div){
                        div.style.backgroundColor = "#FFFFFF";
                        div.classList.remove("data-selected")
                    });
                    return;
                 }
                 let selected_row = parseInt(document.querySelectorAll(".cell-selected")[0].getAttribute("data-cell-row"));
                 let selected_column = parseInt(document.querySelectorAll(".cell-selected")[0].getAttribute("data-cell-column"));
                 if(animation_counter <= events_per_cycle) {
                    if (choices.length > 0){
                        var index = Math.floor(Math.random() * choices.length);
                        var axis = Object.keys(choices[index])[0];
                        var value = Object.values(choices[index])[0];
                        document.querySelectorAll(`div[data-cell-${axis}='${value}']`).forEach(function(div){
                            div.style.backgroundColor = "#ff0000";
                            div.classList.add("data-selected");
                        });
                        if (axis == "row"){
                            eventData.push({"row":value, "column":null, "timestamp":Date.now(),
                            "selected-row":selected_row, "selected-column":selected_column});
                        } else{
                            eventData.push({"row":null, "column":value, "timestamp":Date.now(),
                            "selected-row":selected_row, "selected-column":selected_column});
                        }
                        choices.splice(index, 1);
                    } else {
                        choices = [];
                        for (var i=0; i < 3; i++) choices.push({"row": i});
                        for (var i=0; i < 3; i++) choices.push({"column": i});
                        animation_counter++;
                        console.log(`event per cycle : ${animation_counter}`);
                    }
                 } else {
                      clearInterval(animation_intervalId);
                      console.log(`cycle ${cycle_counter}`);
                      cycle_counter ++;
                      cycle_func();
                      if (cycle_counter >= cycles){
                        end_func(eventData);
                        document.getElementsByClassName("game-container")[0].classList.remove("running");
                        cycle_func();
                        return;
                      }
                      setTimeout(function(){startAnimation(cycle_func, end_func, events_per_cycle, cycles, interval)}, 1000);
                 }
            };
            var _choices = new Array();
            for (let i=0; i < 3; i++) _choices.push({"row": i});
            for (let i=0; i < 3; i++) _choices.push({"column": i});
            var choices = _choices;
            animation_intervalId = null;
            animation_counter = 0;
            animation_intervalId = setInterval(animate, interval);
        }
        var cycle_counter = 0;
        var eventData = [];
        document.getElementsByClassName("game-container")[0].classList.add("running");
        cycle_func();
        setTimeout(function(){startAnimation(cycle_func, end_func, events_per_cycle, cycles, interval)}, 1500); //delete timeout ?
    }

    function createBoard(size){
        for (let i=0; i<size**2; i++){
            var cell = document.createElement('div');
            cell.classList.add("cell", "cell-not-selected");
            cell.setAttribute("data-cell-index", i);
            cell.setAttribute("data-cell-column", i % size);
            cell.setAttribute("data-cell-row", Math.floor(i/size));
            document.getElementsByClassName('game-container')[0].append(cell);
        }
    }

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  function sendData(data){
    socket.emit('event-data', {'data': data});
  }

//  socket.on('connect', function(){
//
//      document.getElementById('data_stream_control').onclick = function(){
//              let action = this.value;
//              socket.emit('start-stream', {'action': action});
//              if(action == "start"){
//                this.value = "stop";
//                this.innerHTML = "Stop Stream";
//              }else{
//                this.value = "start";
//                this.innerHTML = "Start Stream";
//              }
//          };
//      });

   document.getElementById('model-calibration').onclick = function(){
      document.getElementById('model-play').disabled = true;
      if (this.value == 'false'){
          this.value = 'true';
          this.innerHTML = 'Stop Calibration';
          document.getElementById('saved-models').hidden = true;
          document.getElementById('model-save').hidden = false;
          document.getElementById('start-animation').hidden = false;
          createBoard(3);
      }else{
          this.value = 'false';
          this.innerHTML = 'Start Calibration';
          document.getElementById('saved-models').hidden = false;
          document.getElementById('model-save').hidden = true;
          document.getElementById('start-animation').hidden = true;
          document.getElementsByClassName('game-container')[0].innerHTML = "";
      }
   };

   document.getElementById('saved-models').onchange = function(){
        if (this.selectedOptions[0].value != ''){
            document.getElementById('model-play').disabled = false;
        }
   }

   document.getElementById('model-save-name').onkeyup = function(){
        document.getElementById('model-save-submit').disabled = false;
   }

   document.getElementById('model-save-submit').onclick = function(){
        if (document.getElementById('model-save-name').value != ''){
            console.log("save");
            document.getElementById('model-calibration').click();
        }
   }

   function select_cell(size){
     document.querySelectorAll(".cell-selected").forEach(function(div){
        div.classList.remove("cell-selected");
        div.innerHTML = ""
     });
     if (document.getElementsByClassName("game-container")[0].classList.contains("running")){
         let index = Math.floor(Math.random() * size**2);
         let selected_div = document.querySelectorAll(`div[data-cell-index='${index}']`)[0]
         selected_div.classList.add("cell-selected");
         selected_div.innerHTML = "X"
     }
   }

   document.getElementById('start-animation').onclick = function(){
//    interactive parameters - in future versions - hidden dashboard - to setup parameters
        var events_per_cycle = parseInt(document.getElementById("events-data").getAttribute("data-events-per-cycle"))
        var cycles = parseInt(document.getElementById("events-data").getAttribute("data-cycles"))
        var interval = parseInt(document.getElementById("events-data").getAttribute("data-interval"))
        console.log(
          `event animation parameters:\nevents_per_cycle: ${events_per_cycle}\ncycles: ${cycles}\ninterval: ${interval}`
        )
        runAnimationCycle(function(){select_cell(3);}, sendData, events_per_cycle-1, cycles, interval)
   }

   document.getElementById("model-play").onclick = function(){
      createBoard(3);
   }
});
// v events.js - daj animacie
// websocket.js - daj vsetky connection
// budu medzi sebou volat funcs