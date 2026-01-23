import streamlit as st
import pandas as pd
import os
from pathlib import Path

# Configuração da página
st.set_page_config(
    page_title="Provas da Peroba",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado
st.markdown("""
<style>
    .main-header {
        color: #2E86AB;
        text-align: center;
        padding: 1rem;
        border-bottom: 3px solid #A23B72;
    }
    .question-card {
        background-color: #F8F9FA;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #2E86AB;
        margin: 1rem 0;
    }
    .correct-answer {
        background-color: #D4EDDA;
        border-left: 5px solid #28A745;
    }
    .wrong-answer {
        background-color: #F8D7DA;
        border-left: 5px solid #DC3545;
    }
    .stats-card {
        background-color: #E9ECEF;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        margin: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização de variáveis de sessão
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {
        'current_question': 0,
        'selected_answers': {},
        'submitted': False,
        'score': 0,
        'questions_df': None,
        'custom_mode': False
    }

# Pasta de questões
QUESTIONS_FOLDER = "questoes"

def load_questions(file_path, custom_mode=False):
    """Carrega questões do arquivo CSV"""
    try:
        df = pd.read_csv(file_path, header=None, 
                        names=["question", "a", "b", "c", "d", "correct"])
        
        # Limpeza dos dados
        df = df.dropna()
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Resetar estado do quiz
        st.session_state.quiz_state = {
            'current_question': 0,
            'selected_answers': {},
            'submitted': False,
            'score': 0,
            'questions_df': df,
            'custom_mode': custom_mode,
            'total_questions': len(df)
        }
        return df
    except Exception as e:
        st.error(f"Erro ao carregar questões: {e}")
        return None

def display_question(df, index):
    """Exibe uma questão individual"""
    question = df.iloc[index]
    
    st.markdown(f"### Questão {index + 1} de {len(df)}")
    
    # Card da questão
    st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
    st.markdown(f"**{question['question']}**")
    
    # Opções de resposta
    options = ['a', 'b', 'c', 'd']
    option_labels = ['A', 'B', 'C', 'D']
    
    # Verificar se já há resposta selecionada
    selected_key = f"q{index}_selected"
    if selected_key not in st.session_state.quiz_state['selected_answers']:
        st.session_state.quiz_state['selected_answers'][selected_key] = None
    
    # Criar colunas para as opções (2x2)
    col1, col2 = st.columns(2)
    
    for i, (opt, label) in enumerate(zip(options, option_labels)):
        col = col1 if i < 2 else col2
        with col:
            # Criar uma chave única para cada botão de rádio
            if st.button(
                f"{label}) {question[opt]}",
                key=f"q{index}_{opt}",
                use_container_width=True,
                type="primary" if st.session_state.quiz_state['selected_answers'][selected_key] == opt else "secondary"
            ):
                st.session_state.quiz_state['selected_answers'][selected_key] = opt
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botão de submeter resposta individual
    if st.session_state.quiz_state['selected_answers'][selected_key] is not None:
        if st.button("✅ Verificar Resposta", key=f"submit_{index}"):
            check_answer(index, question)
    
    # Mostrar feedback se já foi submetido
    if st.session_state.quiz_state.get(f"feedback_{index}"):
        feedback = st.session_state.quiz_state[f"feedback_{index}"]
        if feedback['correct']:
            st.success(feedback['message'])
        else:
            st.error(feedback['message'])

def check_answer(index, question):
    """Verifica se a resposta está correta"""
    selected_key = f"q{index}_selected"
    selected_answer = st.session_state.quiz_state['selected_answers'].get(selected_key)
    
    if selected_answer:
        correct = selected_answer == question['correct'].lower()
        
        if correct:
            st.session_state.quiz_state['score'] += 1
            message = f"✅ Correto! A resposta {selected_answer.upper()} está certa."
        else:
            message = f"❌ Resposta {selected_answer.upper()} incorreta. A correta é {question['correct'].upper()}."
        
        # Armazenar feedback
        st.session_state.quiz_state[f"feedback_{index}"] = {
            'correct': correct,
            'message': message
        }
        
        st.rerun()

def display_stats():
    """Exibe estatísticas do quiz"""
    df = st.session_state.quiz_state['questions_df']
    total = len(df)
    score = st.session_state.quiz_state['score']
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Questões", f"{total}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'<div class="stats-card">', unsafe_allow_html=True)
        st.metric("Acertos", f"{score}/{total}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'<div class="stats-card">', unsafe_allow_html=True)
        percentage = (score / total * 100) if total > 0 else 0
        st.metric("Percentual", f"{percentage:.1f}%")
        st.markdown('</div>', unsafe_allow_html=True)

def reset_quiz():
    """Reseta o estado do quiz"""
    st.session_state.quiz_state = {
        'current_question': 0,
        'selected_answers': {},
        'submitted': False,
        'score': 0,
        'questions_df': None,
        'custom_mode': False
    }

# Menu lateral
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/test-passed.png", width=80)
    st.title("Provas da Peroba")
    
    menu = st.radio(
        "Navegação",
        ["🏠 Página Inicial", "📝 Quiz", "🔧 Estudo Customizado"]
    )

# Página Inicial
if menu == "🏠 Página Inicial":
    st.markdown('<h1 class="main-header">📚 Provas da Peroba</h1>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Sobre o App
        
        **Provas da Peroba** é uma aplicação interativa de quiz desenvolvida para 
        testar e consolidar conhecimentos em diversas matérias do curso.
        
        ### Funcionalidades
        
        🎯 **Quiz por Matéria**: Teste seus conhecimentos em matérias específicas
        📊 **Feedback Imediato**: Saiba na hora se acertou ou errou
        📁 **Estudo Customizado**: Use seus próprios arquivos CSV
        
        ### Como usar?
        
        1. Na seção **Quiz**, escolha uma matéria
        2. Responda as questões
        3. Receba feedback imediato
        4. Acompanhe seu desempenho
        
        ### Desenvolvido por
        
        [João da Petrobras](https://github.com/joao-petro)
        
        ---
        
        *Criado com ❤️ para auxiliar nos estudos*
        """)

# Página de Quiz
elif menu == "📝 Quiz":
    st.title("📝 Quiz")
    
    # Verificar se a pasta de questões existe
    if not os.path.exists(QUESTIONS_FOLDER):
        st.warning(f"Crie a pasta '{QUESTIONS_FOLDER}' e adicione arquivos CSV com questões.")
        st.info("""
        Estrutura do CSV (sem cabeçalho):
        ```
        "Pergunta?","Opção A","Opção B","Opção C","Opção D","a"
        ```
        Última coluna deve ser a letra da resposta correta (a, b, c, ou d)
        """)
    else:
        # Listar arquivos CSV disponíveis
        csv_files = [f for f in os.listdir(QUESTIONS_FOLDER) if f.endswith('.csv')]
        
        if not csv_files:
            st.warning(f"Nenhum arquivo CSV encontrado na pasta '{QUESTIONS_FOLDER}'.")
        else:
            # Seleção de matéria
            selected_file = st.selectbox(
                "Escolha a matéria:",
                csv_files,
                index=None,
                placeholder="Selecione um arquivo..."
            )
            
            if selected_file:
                file_path = os.path.join(QUESTIONS_FOLDER, selected_file)
                
                # Botão para carregar questões
                if st.button("Carregar Questões") or st.session_state.quiz_state['questions_df'] is not None:
                    if st.session_state.quiz_state['questions_df'] is None:
                        df = load_questions(file_path)
                    else:
                        df = st.session_state.quiz_state['questions_df']
                    
                    if df is not None and len(df) > 0:
                        # Controles de navegação
                        col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                        
                        with col2:
                            if st.button("⏮️ Anterior", disabled=st.session_state.quiz_state['current_question'] == 0):
                                st.session_state.quiz_state['current_question'] -= 1
                                st.rerun()
                        
                        with col3:
                            total = len(df)
                            current = st.session_state.quiz_state['current_question']
                            if st.button("Próxima ⏭️", disabled=current >= total - 1):
                                st.session_state.quiz_state['current_question'] += 1
                                st.rerun()
                        
                        # Exibir questão atual
                        current_idx = st.session_state.quiz_state['current_question']
                        display_question(df, current_idx)
                        
                        # Exibir estatísticas
                        display_stats()
                        
                        # Botão para reiniciar
                        if st.button("🔄 Reiniciar Quiz"):
                            reset_quiz()
                            st.rerun()

# Página de Estudo Customizado
elif menu == "🔧 Estudo Customizado":
    st.title("🔧 Estudo Customizado")
    
    st.markdown("""
    ### Carregue suas próprias questões
    
    Faça upload de um arquivo CSV com suas questões no formato:
    
    ```
    "Enunciado da questão","Opção A","Opção B","Opção C","Opção D","letra_correta"
    ```
    
    **Importante**: O arquivo não deve ter cabeçalho!
    """)
    
    uploaded_file = st.file_uploader(
        "Escolha um arquivo CSV",
        type=['csv'],
        help="Arquivo CSV sem cabeçalho"
    )
    
    if uploaded_file is not None:
        try:
            # Carregar questões do arquivo enviado
            df = pd.read_csv(uploaded_file, header=None, 
                           names=["question", "a", "b", "c", "d", "correct"])
            
            if df.empty:
                st.warning("O arquivo está vazio.")
            else:
                # Botão para carregar questões
                if st.button("▶️ Iniciar Quiz Personalizado"):
                    load_questions(uploaded_file, custom_mode=True)
                    st.rerun()
                
                # Se já houver questões carregadas
                if st.session_state.quiz_state['questions_df'] is not None:
                    df = st.session_state.quiz_state['questions_df']
                    
                    # Controles de navegação
                    col1, col2, col3, col4 = st.columns([2, 1, 1, 2])
                    
                    with col2:
                        if st.button("⏮️ Anterior", key="prev_custom", 
                                   disabled=st.session_state.quiz_state['current_question'] == 0):
                            st.session_state.quiz_state['current_question'] -= 1
                            st.rerun()
                    
                    with col3:
                        total = len(df)
                        current = st.session_state.quiz_state['current_question']
                        if st.button("Próxima ⏭️", key="next_custom", 
                                   disabled=current >= total - 1):
                            st.session_state.quiz_state['current_question'] += 1
                            st.rerun()
                    
                    # Exibir questão atual
                    current_idx = st.session_state.quiz_state['current_question']
                    display_question(df, current_idx)
                    
                    # Exibir estatísticas
                    display_stats()
                    
                    # Botão para reiniciar
                    if st.button("🔄 Reiniciar Quiz", key="reset_custom"):
                        reset_quiz()
                        st.rerun()
        
        except Exception as e:
            st.error(f"Erro ao processar o arquivo: {e}")
            st.info("""
            Verifique o formato do arquivo. Deve ser:
            - Sem cabeçalho
            - 6 colunas: pergunta, A, B, C, D, resposta_correta
            - A resposta correta deve ser 'a', 'b', 'c' ou 'd'
            """)

# Rodapé
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
    Provas da Peroba • Desenvolvido para auxiliar nos estudos
    </div>
    """,
    unsafe_allow_html=True
)