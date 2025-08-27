import streamlit as st
import ChessEngine
import base64

# Board setup
WIDTH = HEIGHT = 480
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION

pieces = ['wP','wR','wB','wN','wQ','wK','bP','bR','bN','bB','bQ','bK']
piece_images = {}

# --- Load images once ---
def load_images():
    for piece in pieces:
        with open(f"images/{piece}.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            piece_images[piece] = b64

# --- Draw board as buttons ---
def draw_board(gs):
    for r in range(DIMENSION):
        cols = st.columns(DIMENSION, gap="small")
        for c in range(DIMENSION):
            piece = gs.board[r][c]
            color = "#EEE" if (r+c) % 2 == 0 else "#888"

            if piece != "--":
                img_html = f"""
                <div style="background:{color};width:{SQ_SIZE}px;height:{SQ_SIZE}px;
                            display:flex;align-items:center;justify-content:center;">
                    <img src="data:image/png;base64,{piece_images[piece]}"
                         style="width:{SQ_SIZE*0.9}px;height:{SQ_SIZE*0.9}px;">
                </div>
                """
            else:
                img_html = f"""
                <div style="background:{color};width:{SQ_SIZE}px;height:{SQ_SIZE}px;"></div>
                """

            # Use a button with HTML inside
            if cols[c].button("", key=f"{r},{c}"):
                handle_square_click(r, c)

            cols[c].markdown(img_html, unsafe_allow_html=True)

# --- Handle a click on a square ---
def handle_square_click(r, c):
    gs = st.session_state.gs
    st.session_state.playerClicks.append((r, c))

    if len(st.session_state.playerClicks) == 2:
        sr, sc = st.session_state.playerClicks[0]
        er, ec = st.session_state.playerClicks[1]
        move = ChessEngine.Move((sr, sc), (er, ec), gs.board)

        if move in st.session_state.validMoves:
            gs.makeMove(move)
            st.session_state.validMoves = gs.getValidMoves()
        else:
            st.warning("Invalid move")

        st.session_state.playerClicks = []

# --- Main app ---
def main():
    st.set_page_config(page_title="Chess", layout="centered")

    if "gs" not in st.session_state:
        st.session_state.gs = ChessEngine.GameState()
        st.session_state.validMoves = st.session_state.gs.getValidMoves()
        st.session_state.playerClicks = []

    st.title("♟️ Streamlit Chess")
    draw_board(st.session_state.gs)

    if st.button("♻️ Restart game"):
        st.session_state.gs = ChessEngine.GameState()
        st.session_state.validMoves = st.session_state.gs.getValidMoves()
        st.session_state.playerClicks = []

if __name__ == "__main__":
    if not piece_images:
        load_images()
    main()
