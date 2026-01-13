<div align="center">

# 🚀 DevTracker
### Seu Gerente de Projetos Técnico movido a IA

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django)
![AI](https://img.shields.io/badge/Gemini-Flash-orange?style=for-the-badge&logo=google)
![Status](https://img.shields.io/badge/Status-Online-success?style=for-the-badge)

[Ver Demo Online](https://ghsiqueira.pythonanywhere.com)

</div>

---

## 💡 Sobre o Projeto

O **DevTracker** não é apenas um To-Do list. É um sistema que utiliza **Inteligência Artificial Generativa (Google Gemini)** para atuar como um *Tech Lead* virtual.

Ao cadastrar uma ideia de projeto, o sistema analisa a descrição, decide a complexidade técnica e gera automaticamente um **WBS (Work Breakdown Structure)** completo, com tarefas técnicas, prioridades calibradas e cronograma sequencial.

---

## 🔥 Funcionalidades Principais

### 🧠 IA & Automação
* **Prompt Engineering Avançado:** O sistema distingue entre projetos simples (ex: "Lista de Compras") e complexos, ajustando a quantidade e profundidade técnica das tarefas geradas.
* **Calibragem de Prioridade:** Lógica estrita para evitar o problema de "tudo é urgente", limitando tarefas *High Priority* a apenas 20% do backlog (blockers e infraestrutura).
* **Agendamento Inteligente:** A IA estima o `days_from_start` para criar um cronograma realista, não jogando todas as tarefas para o mesmo dia.

### 🎨 UX/UI Moderna
* **Interface Limpa:** Design responsivo com Bootstrap 5.
* **Smart Description:** Sistema de "Read More/Less" para descrições longas, mantendo o layout organizado.
* **Feedback Visual:** Badges de contagem de tarefas, barras de progresso dinâmicas e alertas de prazos vencidos.

### 🛡️ Segurança & Infraestrutura
* **Proteção de Dados:** Variáveis de ambiente (`python-dotenv`) para blindagem de API Keys.
* **Django 6:** Utilizando a versão mais recente e performática do framework.
* **Deploy:** Hospedado e configurado em ambiente Linux (PythonAnywhere).

---

## 🛠️ Stack Tecnológica

| Categoria | Tecnologia |
| :--- | :--- |
| **Backend** | Python 3.12, Django 6.0.1 |
| **AI Model** | Google Gemini 1.5 Flash |
| **Frontend** | HTML5, CSS3, Bootstrap 5, Jinja2 |
| **Database** | SQLite3 (Dev/Prod) |
| **Deploy** | PythonAnywhere (WSGI) |

---

## 🚀 Como rodar localmente

Se você deseja clonar e testar este projeto na sua máquina:

```bash
# 1. Clone o repositório
git clone https://github.com/ghsiqueira/devtracker.git

# 2. Entre na pasta
cd devtracker

# 3. Crie e ative o ambiente virtual
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 4. Instale as dependências
pip install -r requirements.txt

# 5. Configure as Variáveis de Ambiente
# Crie um arquivo .env na raiz e adicione sua chave:
# GEMINI_API_KEY=sua_chave_aqui
# SECRET_KEY=sua_chave_secreta
# DEBUG=True

# 6. Prepare o Banco de Dados
python manage.py migrate

# 7. Inicie o Servidor
python manage.py runserver
```

Acesse em: http://127.0.0.1:8000

<div align="center">
Desenvolvido com 💙 por Gabriel Siqueira
</div>
