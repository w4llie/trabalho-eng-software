// Função para abrir o formulário de anúncio
function openHouseForm() {
    document.getElementById('houseForm').style.display = 'block';
}

// Função para fechar o formulário de anúncio
function closeHouseForm() {
    document.getElementById('houseForm').style.display = 'none';
}

// Função para abrir o formulário de interesse
function openInterestForm() {
    document.getElementById('interestForm').style.display = 'block';
}

// Função para fechar o formulário de interesse
function closeForm() {
    document.getElementById('interestForm').style.display = 'none';
}

// Função para adicionar o anúncio à tela de compartilhamento
function submitAd(event) {
    event.preventDefault();

    const announcerName = document.getElementById('announcerName').value;
    const rentalPrice = document.getElementById('rentalPrice').value;
    const address = document.getElementById('address').value;
    const neighborhood = document.getElementById('neighborhood').value;
    const description = document.getElementById('description').value;

    const adContainer = document.getElementById('adsContainer');

    // Criar o novo anúncio
    const adElement = document.createElement('div');
    adElement.classList.add('ad');
    adElement.innerHTML = `
        <h3>${announcerName}</h3>
        <p><strong>Preço:</strong> R$ ${rentalPrice}</p>
        <p><strong>Endereço:</strong> ${address}</p>
        <p><strong>Bairro:</strong> ${neighborhood}</p>
        <p><strong>Descrição:</strong> ${description}</p>
        <button class="btn" onclick="openInterestForm()">Mostrar Interesse</button>
        <button class="btn" onclick="deleteAd(this)">Deletar Anúncio</button>
    `;

    // Adicionar o anúncio à tela
    adContainer.appendChild(adElement);

    // Fechar o formulário após a adição
    closeHouseForm();
}

// Função para deletar o anúncio
function deleteAd(button) {
    const adElement = button.parentElement;
    adElement.remove();
}

// Função para enviar o formulário de interesse (para exemplo, apenas fecha o formulário)
function handleSubmit(event) {
    event.preventDefault();

    const fullName = document.getElementById('fullName').value;
    const contactNumber = document.getElementById('contactNumber').value;
    const email = document.getElementById('email').value;

    // Aqui você pode adicionar a lógica de envio dos dados do formulário de interesse
    console.log('Interesse enviado:', fullName, contactNumber, email);

    // Fechar o formulário após envio
    closeForm();
}
