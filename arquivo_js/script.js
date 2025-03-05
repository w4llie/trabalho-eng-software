// Função para alternar entre as telas de Login e Cadastro
function toggleForms() {
    const loginForm = document.getElementById("login-form");
    const cadastroForm = document.getElementById("cadastro-form");
    
    // Alterna a exibição dos formulários
    if (loginForm.style.display === "none") {
        loginForm.style.display = "block";
        cadastroForm.style.display = "none";
    } else {
        loginForm.style.display = "none";
        cadastroForm.style.display = "block";
    }
}

document.getElementById("login-form-element").addEventListener("submit", function(event) {
    event.preventDefault();
    
    // Coleta os valores dos campos
    const email = document.getElementById("email").value;
    const senha = document.getElementById("senha").value;
    
    // Simulação de validação do login (substitua com a lógica real)
    if (email === "user@example.com" && senha === "senha123") {
        window.location.href = "tela_inicial.html";  // Redireciona para a página principal
    } else {
        alert("Credenciais inválidas.");
    }
});