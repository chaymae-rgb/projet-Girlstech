function setCode(value){const t=document.getElementById("code");if(t)t.value=value;}

let adaSteps = [];
let adaIndex = 0;

document.addEventListener("DOMContentLoaded", () => {
    const guide = document.querySelector(".ada-guide");
    if (guide) {
        try {
            adaSteps = JSON.parse(guide.dataset.steps);
            adaIndex = 0;
            document.getElementById("adaText").textContent = adaSteps[0];
        } catch(e) {}
    }
});

function nextAdaStep(){
    if(!adaSteps.length) return;
    adaIndex++;
    const text = document.getElementById("adaText");
    const btn = document.getElementById("adaNext");
    if(adaIndex < adaSteps.length){
        text.textContent = adaSteps[adaIndex];
        if(adaIndex === adaSteps.length - 1) btn.textContent = "Commencer le quiz ✨";
    } else {
        document.querySelector(".ada-guide").style.display = "none";
        document.getElementById("quizCard").scrollIntoView({behavior:"smooth"});
    }
}

function toggleChat(){
    document.getElementById("chatPanel").classList.toggle("open");
}

function askQuick(q){
    document.getElementById("chatInput").value = q;
    sendQuestion();
}

async function sendQuestion(){
    const input = document.getElementById("chatInput");
    const body = document.getElementById("chatBody");
    const question = input.value.trim();
    if(!question) return;
    body.innerHTML += `<div class="user-msg">${question}</div>`;
    input.value = "";
    const response = await fetch("/chatbot", {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({question})
    });
    const data = await response.json();
    body.innerHTML += `<div class="bot-msg">${data.answer}</div>`;
    body.scrollTop = body.scrollHeight;
}
