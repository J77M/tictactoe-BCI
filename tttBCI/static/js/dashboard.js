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
        var timestamps = [] // change to json : timestamps : row, col
        var animate = function(){
             if(document.querySelectorAll(".data-selected").length != 0){
                document.querySelectorAll(".data-selected").forEach(function(div){
                    div.style.backgroundColor = "#FFFFFF";
                    div.classList.remove("data-selected")
                })
                return;
             }
             if(animation_counter <= events_per_cycle) {
                  animation_counter++;
                  let index = Math.floor(Math.random() * 3) // todo: sizexsize value
                  if(Math.floor(Math.random() * 2) == 0){
                    document.querySelectorAll(`div[data-cell-row='${index}']`).forEach(function(div){
                    div.style.backgroundColor = "#ff0000";
                    div.classList.add("data-selected");
                    })
                  } else{
                    document.querySelectorAll(`div[data-cell-column='${index}']`).forEach(function(div){
                    div.style.backgroundColor = "#ff0000";
                    div.classList.add("data-selected");
                    })
                  }
//                  timestamps.push(animation_counter);
             } else {
                  clearInterval(animation_intervalId);
//                  console.log(timestamps);
                  cycle_counter ++;
                  cycle_func();
                  if (cycle_counter >= cycles){
                    end_func();
                    return;
                  }
                  setTimeout(function(){startAnimation(cycle_func, end_func, events_per_cycle, cycles, interval)}, interval*2);
             }
        };
        animation_intervalId = null;
        animation_counter = 0;
        animation_intervalId = setInterval(animate, interval);
    }
    var cycle_counter = 0;
    startAnimation(cycle_func, end_func, events_per_cycle, cycles, interval);
}

function createBoard(size){
    for (let i=0; i<size**2; i++){
        var cell = document.createElement('div');
        cell.classList.add("cell", "not-selected");
        cell.setAttribute("data-cell-index", i);
        cell.setAttribute("data-cell-column", i % size);
        cell.setAttribute("data-cell-row", Math.floor(i/size));
        document.getElementsByClassName('game-container')[0].append(cell);
    }
//    document.querySelectorAll(".not-selected").forEach(function(div){
//        div.onclick = function(){
//            if (! this.classList.contains("disabled")){
//                this.innerHTML = "X";
//                this.classList.remove("not-selected");
//            }
//            document.querySelectorAll(".not-selected").forEach(function(div){
//            div.classList.add("disabled");
//            })
//        }
//   })
}

document.addEventListener('DOMContentLoaded', () => {

  var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

  socket.on('connect', function(){

      document.getElementById('data_stream_control').onclick = function(){
              let action = this.value;
              socket.emit('start-stream', {'action': action});
              if(action == "start"){
                this.value = "stop";
                this.innerHTML = "Stop Stream";
              }else{
                this.value = "start";
                this.innerHTML = "Start Stream";
              }
          };
      });

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

   document.getElementById('start-animation').onclick = function(){
        setTimeout(function(){runAnimationCycle(function(){console.log("cycle");},
         function(){console.log("end");}, 10, 5, 200)}, 1000);
   }

   document.getElementById("model-play").onclick = function(){
      createBoard(3);
   }
});
// v events.js - daj animacie
// websocket.js - daj vsetky connection
// budu medzi sebou volat funcs