let casas = [];


function exibirResidencias() {
    const container = document.getElementById('residencias-container');
    const mensagemVazia = document.getElementById('mensagem-vazia');
    container.innerHTML = ''; // Limpa o conteúdo

    if (casas.length === 0) {
        mensagemVazia.style.display = 'block'; // Exibe a mensagem se não houver casas
    } else {
        mensagemVazia.style.display = 'none'; // Oculta a mensagem se houver casas
        casas.forEach(casa => {
            const div = document.createElement('div');
            div.classList.add('residencia');
            div.innerHTML = `
                <img src="${casa.imagem}" alt="Imagem da residência">
                <h3>${casa.nome}</h3>
                <p>${casa.endereco}</p>
                <p>${casa.bairro}</p>
                <p>R$ ${casa.valor}</p>
                <a href="detalhes.html?id=${casa.id}">
                    <button>Ver Detalhes</button>
                </a>
            `;
            container.appendChild(div);
        });
    }
}

// Carrega as residências ao carregar a página
window.onload = () => {
    exibirResidencias();
};
