document.addEventListener('DOMContentLoaded', () => {

    /* ============================================================
       ACORDEÕES (Sinopse / Ficha Técnica)
    ============================================================ */
    const accordions = document.querySelectorAll('.section-toggle');

    accordions.forEach(acc => {
        const header = acc.querySelector('.toggle-header');
        const content = acc.querySelector('.toggle-content');
        if (!header || !content) return;

        content.style.display = 'none';

        header.addEventListener('click', () => {
            const isOpen = header.classList.contains('active');

            // Fecha todos
            accordions.forEach(a => {
                const h = a.querySelector('.toggle-header');
                const c = a.querySelector('.toggle-content');
                if (h) h.classList.remove('active');
                if (c) c.style.display = 'none';
            });

            // Abre o clicado
            if (!isOpen) {
                header.classList.add('active');
                content.style.display = 'block';
            }
        });
    });



    /* ============================================================
       FORMULÁRIO DE AVALIAÇÃO (Botão superior "Avaliar")
    ============================================================ */
    const btnAvaliar   = document.getElementById('btn-avaliar');
    const formAvaliacao = document.getElementById('form-avaliacao');

    function toggleForm() {
        const isHidden = !formAvaliacao || formAvaliacao.style.display === 'none' || formAvaliacao.style.display === '';
        formAvaliacao.style.display = isHidden ? 'block' : 'none';
        if (btnAvaliar) {
            btnAvaliar.textContent = isHidden ? '✖ Fechar' : '⭐ Avaliar';
        }
    }

    if (btnAvaliar && formAvaliacao) {
        btnAvaliar.addEventListener('click', toggleForm);
    } else {
        if (!btnAvaliar) console.warn("scripts.js: botão '#btn-avaliar' não encontrado.");
        if (!formAvaliacao) console.warn("scripts.js: '#form-avaliacao' não encontrado.");
    }



    /* ============================================================
       BOTÃO "Adicionar" (dentro da área de avaliações)
    ============================================================ */
    const btnAddReview = document.getElementById('add-review-btn');

    if (btnAddReview && formAvaliacao) {
        btnAddReview.addEventListener('click', () => {
            const isHidden = formAvaliacao.style.display === 'none' || formAvaliacao.style.display === '';
            formAvaliacao.style.display = isHidden ? 'block' : 'none';
        });
    }



    /* ============================================================
        SISTEMA DE ESTRELAS (Rating)
    ============================================================ */
    const starBox = document.getElementById('star-selector');
    // Agora o nome do input é 'estrelas'
    const ratingInput = document.querySelector("input[name='estrelas']"); 

    if (starBox && ratingInput) {

        // As estrelas agora usam data-star (conforme o HTML)
        const stars = starBox.querySelectorAll('span[data-star]'); 

        const paintStars = (value) => {
            stars.forEach(star => {
                const starValue = Number(star.dataset.star);
                // Classe 'selected' é o que deve mudar a cor da estrela (você deve ter isso no seu CSS)
                star.classList.toggle('selected', starValue <= value); 
            });
        };

        // Clique na estrela
        stars.forEach(star => {
            star.addEventListener('click', () => {
                const value = Number(star.dataset.star);
                // Atualiza o campo oculto que será enviado
                ratingInput.value = value; 
                paintStars(value);
            });

            // Hover visual (Muda a cor ao passar o mouse)
            star.addEventListener('mouseover', () => {
                const value = Number(star.dataset.star);
                paintStars(value);
            });
        });

        // Saiu do container → volta ao valor registrado (se houver)
        starBox.addEventListener('mouseout', () => {
            const current = Number(ratingInput.value) || 0;
            paintStars(current);
        });

        // Inicializa com valor 0
        paintStars(Number(ratingInput.value) || 0);

    } else {
        if (!starBox) console.warn("scripts.js: '#star-selector' não encontrado.");
        if (!ratingInput) console.warn('scripts.js: input[name="estrelas"] não encontrado.');
    }

});

function toggleComentarios(num) {

    // exibe caixa inline
    const bloco = document.getElementById("cbox-" + num);
    if (bloco){
        bloco.style.display = bloco.style.display === "block" ? "none" : "block";
    }

    // define valor do input
    document.getElementById("posicao_paragrafo").value = num;

    // abre modal
    const modal = new bootstrap.Modal(document.getElementById("modalComentario"));
    modal.show();
}

document.addEventListener("DOMContentLoaded", () => {
    const bubbles = document.querySelectorAll(".bubble");
    bubbles.forEach(b => {
        b.onclick = () => toggleComentarios(parseInt(b.dataset.pos));
    });
});

/* ==========================================================
   COMENTÁRIO POR TRECHO — CAPTURA DA SELEÇÃO
========================================================== */

let btnTrecho = null;

function ensureTrechoButton() {
    if (!btnTrecho) {
        btnTrecho = document.createElement("button");
        btnTrecho.className = "btn-comentar-trecho hidden";
        btnTrecho.textContent = "Comentar trecho";
        document.body.appendChild(btnTrecho);
    }
    return btnTrecho;
}

// Detecta seleção de texto
document.addEventListener("mouseup", () => {
    const selection = window.getSelection().toString().trim();
    const btn = ensureTrechoButton();

    // Sem trecho -> esconde
    if (!selection || selection.length < 3) {
        btn.classList.add("hidden");
        return;
    }

    // Mostra botão
    btn.classList.remove("hidden");

    // Ação do botão → abre modal
    btn.onclick = () => {
        const modalInput = document.getElementById("trecho_selecionado");
        const posInput = document.getElementById("posicao_paragrafo");
        const modal = new bootstrap.Modal(document.getElementById("modalComentario"));

        modalInput.value = selection;
        posInput.value = 0; // 0 = comentário geral do trecho, não parágrafo
        modal.show();
    };
});

// Se o leitor clicar em qualquer lugar -> esconder botão
document.addEventListener("mousedown", () => {
    if (btnTrecho) btnTrecho.classList.add("hidden");
});



