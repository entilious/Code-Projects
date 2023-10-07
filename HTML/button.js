const button = document.querySelector("input");
const paragraph = document.querySelector("a");

button.addEventListener("click", updateButton);

function updateButton() {
  if (button.value === "Start machine") {
    button.value = "Stop machine";
    paragraph.textContent = "The machine has started!";
  } else {
    button.value = 0;
    paragraph.textContent = "The machine is stopped.";
  }
}