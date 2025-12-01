console.log("JS de voz carregado");

(function() {

    const micBtn = document.querySelector(".mic-button");
    if (!micBtn) return;

    if (!("webkitSpeechRecognition" in window)) {
        micBtn.addEventListener("click", () => {
            alert("⚠️ Seu navegador não suporta comandos de voz.");
        });
        return;
    }

    const rec = new webkitSpeechRecognition();
    rec.lang = "pt-BR";
    rec.continuous = false;
    rec.interimResults = false;

    function animacaoOn() {
        micBtn.classList.add("listening");
    }
    function animacaoOff() {
        micBtn.classList.remove("listening");
    }

    micBtn.addEventListener("click", () => {
        animacaoOn();
        rec.start();
    });

    rec.onresult = (event) => {
        animacaoOff();

        const comando = event.results[0][0].transcript.toLowerCase().trim();
        console.log("🎤 Texto reconhecido:", comando);

        fetch(`/voz/comando/?texto=${encodeURIComponent(comando)}`)
            .then(r => r.json())
            .then(data => {

                if (data.redirect) {
                    window.location.href = data.redirect;
                    return;
                }

                if (data.msg) {
                    alert(data.msg);
                }
            })
            .catch(() => alert("⚠️ Erro inesperado ao processar comando"));
    };

    rec.onerror = (e) => {
        animacaoOff();
        
        if (e.error === "no-speech") {
            alert("Nenhum áudio detectado. Tente falar mais perto 😊");
            return;
        }

        if (e.error === "audio-capture") {
            alert("Ative o microfone para usar comandos de voz.");
            return;
        }

        alert("Não consegui entender. Tente novamente.");
    };

})();