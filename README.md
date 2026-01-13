# 🚀 DevTracker - AI Powered Task Manager

Gerenciador de tarefas inteligente desenvolvido com **Django 6** e **Google Gemini AI**. O sistema analisa a descrição dos seus projetos e gera automaticamente um cronograma completo de tarefas técnicas.

## ✨ Funcionalidades
* **Geração Inteligente:** Integração com a API `gemini-flash-latest` para planejar backlogs baseados na complexidade do projeto.
* **Contador de Tasks:** Visualização clara da quantidade de tarefas geradas ao lado da descrição.
* **Descrição Expansível:** Sistema de "Read More" para manter a interface limpa mesmo com descrições longas.
* **Segurança:** Uso de variáveis de ambiente para proteção de chaves sensíveis.

## 🛠️ Tecnologias
* Python 3.12
* Django 6.0.1
* Google Generative AI (Gemini API)
* Bootstrap 5 (UI)
* SQLite (Database)

## 🚀 Como rodar o projeto localmente
1. Clone o repositório: `git clone https://github.com/ghsiqueira/devtracker.git`
2. Crie uma venv: `python -m venv venv`
3. Ative a venv: `.\venv\Scripts\activate` (Windows)
4. Instale os requisitos: `pip install -r requirements.txt`
5. Crie um arquivo `.env` com sua `GEMINI_API_KEY`.
6. Execute: `python manage.py migrate` e `python manage.py runserver`