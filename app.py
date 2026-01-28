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
.progress-container {
    margin: 2rem 0;
    padding: 1rem;
    background-color: #F8F9FA;
    border-radius: 10px;
}
.warning-box {
    background-color: #FFF3CD;
    border-left: 5px solid #FFC107;
    padding: 1rem;
    border-radius: 5px;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Inicialização de variáveis de sessão
if 'quiz_state' not in st.session_state:
    st.session_state.quiz_state = {
        'current_question': 0,
        'selected_answers': {},
        'submitted_answers': {},
        'questions_df': None,
        'custom_mode': False,
        'total_questions': 0,
        'answered_count': 0,
        'show_results': False  # Nova flag para controlar exibição de resultados
    }

# Pasta de questões
QUESTIONS_FOLDER = "questoes"

def load_questions(file_path, custom_mode=False):
    """Carrega questões do arquivo CSV"""
    try:
        # Se for modo customizado (upload), usar o objeto diretamente
        if custom_mode:
            df = pd.read_csv(file_path, header=None, 
                            names=["question", "a", "b", "c", "d", "correct"])
        else:
            # Se for arquivo local, usar o caminho
            df = pd.read_csv(file_path, header=None, 
                            names=["question", "a", "b", "c", "d", "correct"])
        
        # Limpeza dos dados
        df = df.dropna()
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
        
        # Resetar estado do quiz
        st.session_state.quiz_state = {
            'current_question': 0,
            'selected_answers': {},
            'submitted_answers': {},
            'questions_df': df,
            'custom_mode': custom_mode,
            'total_questions': len(df),
            'answered_count': 0,
            'show_results': False
        }
        return df
    except Exception as e:
        st.error(f"Erro ao carregar questões: {e}")
        return None

def display_question(df, index):
    """Exibe uma questão individual"""
    question = df.iloc[index]
    
    st.markdown(f"### Questão {index + 1} de {len(df)}")
    
    # Barra de progresso
    progress_value = (index + 1) / len(df)
    st.progress(progress_value, text=f"Progresso: {index + 1}/{len(df)} questões")
    
    # Card da questão
    st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
    st.markdown(f"**{question['question']}**")
    
    # Opções de resposta
    options = ['a', 'b', 'c', 'd']
    option_labels = ['A', 'B', 'C', 'D']
    
    # Verificar se já há resposta selecionada
    selected_key = f"q{index}"
    if selected_key not in st.session_state.quiz_state['selected_answers']:
        st.session_state.quiz_state['selected_answers'][selected_key] = None
    
    # Criar colunas para as opções (2x2)
    col1, col2 = st.columns(2)
    
    for i, (opt, label) in enumerate(zip(options, option_labels)):
        col = col1 if i < 2 else col2
        with col:
            if st.button(
                f"{label}. {question[opt]}",
                key=f"q{index}_{opt}",
                use_container_width=True,
                type="primary" if st.session_state.quiz_state['selected_answers'][selected_key] == opt else "secondary"
            ):
                st.session_state.quiz_state['selected_answers'][selected_key] = opt
                
                # Verificar resposta imediatamente ao selecionar
                check_answer(index, question)
                st.rerun()
    
    # Mostrar feedback se já foi respondida
    if selected_key in st.session_state.quiz_state['submitted_answers']:
        feedback = st.session_state.quiz_state['submitted_answers'][selected_key]
        if feedback['correct']:
            st.success(f"✅ {feedback['message']}")
        else:
            st.error(f"❌ {feedback['message']}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Botões de navegação
    col_prev, col_next, col_finish = st.columns([2, 2, 3])
    
    with col_prev:
        if st.button("⏮️ Anterior", 
                    disabled=st.session_state.quiz_state['current_question'] == 0,
                    use_container_width=True):
            st.session_state.quiz_state['current_question'] -= 1
            st.rerun()
    
    with col_next:
        total = len(df)
        current = st.session_state.quiz_state['current_question']
        if st.button("Próxima ⏭️", 
                    disabled=current >= total - 1,
                    use_container_width=True):
            st.session_state.quiz_state['current_question'] += 1
            st.rerun()
    
    with col_finish:
        # Botão para finalizar quiz (disponível em qualquer questão)
        if st.button("🏁 Finalizar Quiz", 
                    use_container_width=True,
                    type="primary"):
            st.session_state.quiz_state['show_results'] = True
            st.rerun()

def check_answer(index, question):
    """Verifica se a resposta está correta e armazena o resultado"""
    selected_key = f"q{index}"
    selected_answer = st.session_state.quiz_state['selected_answers'].get(selected_key)
    
    if selected_answer:
        correct = selected_answer == question['correct'].lower()
        
        if correct:
            message = f"Correto! A resposta {selected_answer.upper()} está certa."
        else:
            message = f"Resposta {selected_answer.upper()} incorreta. A correta é {question['correct'].upper()}."
        
        # Armazenar feedback
        st.session_state.quiz_state['submitted_answers'][selected_key] = {
            'correct': correct,
            'message': message
        }
        
        # Contar questões respondidas
        answered = len([k for k in st.session_state.quiz_state['submitted_answers'] 
                       if k.startswith('q')])
        st.session_state.quiz_state['answered_count'] = answered

def reset_quiz():
    """Reseta o estado do quiz"""
    st.session_state.quiz_state = {
        'current_question': 0,
        'selected_answers': {},
        'submitted_answers': {},
        'questions_df': None,
        'custom_mode': False,
        'total_questions': 0,
        'answered_count': 0,
        'show_results': False
    }

def display_results():
    """Exibe resultados ao final do quiz"""
    df = st.session_state.quiz_state['questions_df']
    total = len(df)
    
    # Contar acertos e questões não respondidas
    correct_count = 0
    unanswered_questions = []
    
    for i in range(total):
        key = f"q{i}"
        if key in st.session_state.quiz_state['submitted_answers']:
            if st.session_state.quiz_state['submitted_answers'][key]['correct']:
                correct_count += 1
        else:
            unanswered_questions.append(i + 1)  # +1 para exibir número da questão (não índice)
    
    st.markdown("---")
    st.markdown("### 📊 Resultado Final")
    
    # Mostrar aviso se houver questões não respondidas
    if unanswered_questions:
        st.markdown(f'<div class="warning-box">', unsafe_allow_html=True)
        st.warning(f"⚠️ Você deixou **{len(unanswered_questions)} questão(ões)** em branco.")
        if len(unanswered_questions) <= 10:  # Mostrar apenas se forem poucas questões
            st.write(f"Questões não respondidas: {', '.join(map(str, unanswered_questions))}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Estatísticas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Questões", total)
    
    with col2:
        answered_count = total - len(unanswered_questions)
        st.metric("Questões Respondidas", f"{answered_count}/{total}")
    
    with col3:
        st.metric("Acertos", f"{correct_count}/{answered_count if answered_count > 0 else total}")
    
    # Percentuais
    col1, col2 = st.columns(2)
    
    with col1:
        answered_count = total - len(unanswered_questions)
        completion_percentage = (answered_count / total * 100) if total > 0 else 0
        st.metric("Taxa de Conclusão", f"{completion_percentage:.1f}%")
    
    with col2:
        answered_count = total - len(unanswered_questions)
        accuracy_percentage = (correct_count / answered_count * 100) if answered_count > 0 else 0
        st.metric("Taxa de Acerto", f"{accuracy_percentage:.1f}%")
    
    # Botões de ação
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔄 Reiniciar Quiz", use_container_width=True):
            reset_quiz()
            st.rerun()
    
    with col2:
        if unanswered_questions and st.button("📝 Voltar para Responder", use_container_width=True):
            st.session_state.quiz_state['show_results'] = False
            # Voltar para a primeira questão não respondida
            st.session_state.quiz_state['current_question'] = unanswered_questions[0] - 1
            st.rerun()

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
        🏁 **Finalização Flexível**: Finalize o quiz a qualquer momento
        
        ### Como usar?
        
        1. Na seção **Quiz**, escolha uma matéria
        2. Responda as questões
        3. Receba feedback imediato
        4. Acompanhe seu progresso
        5. Finalize quando quiser ou responda todas as questões
        
        ### Problemas ou Sugestões?
        
        Mande uma mensagem no Teams (GFGQ)
        
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
                col_load, col_reset = st.columns([3, 1])
                with col_load:
                    if st.button("▶️ Iniciar Quiz", use_container_width=True):
                        df = load_questions(file_path)
                        if df is not None:
                            st.success(f"Quiz '{selected_file}' carregado com {len(df)} questões!")
                            st.rerun()
                
                with col_reset:
                    if st.button("🔄 Reiniciar", use_container_width=True):
                        reset_quiz()
                        st.rerun()
                
                # Se já houver questões carregadas
                if st.session_state.quiz_state['questions_df'] is not None:
                    df = st.session_state.quiz_state['questions_df']
                    
                    # Verificar se deve exibir resultados
                    if st.session_state.quiz_state['show_results']:
                        display_results()
                    else:
                        # Exibir questão atual
                        current_idx = st.session_state.quiz_state['current_question']
                        display_question(df, current_idx)

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
            # Botões de controle
            col_load, col_reset = st.columns([3, 1])
            
            with col_load:
                if st.button("▶️ Iniciar Quiz Personalizado", use_container_width=True):
                    df = load_questions(uploaded_file, custom_mode=True)
                    if df is not None:
                        st.success(f"Quiz carregado com {len(df)} questões!")
                        st.rerun()
            
            with col_reset:
                if st.button("🔄 Reiniciar", use_container_width=True):
                    reset_quiz()
                    st.rerun()
            
            # Se já houver questões carregadas E for modo customizado
            if (st.session_state.quiz_state['questions_df'] is not None and 
                st.session_state.quiz_state['custom_mode']):
                
                df = st.session_state.quiz_state['questions_df']
                
                # Verificar se deve exibir resultados
                if st.session_state.quiz_state['show_results']:
                    display_results()
                else:
                    # Exibir questão atual
                    current_idx = st.session_state.quiz_state['current_question']
                    display_question(df, current_idx)
        
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