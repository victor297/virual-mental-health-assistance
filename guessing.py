import streamlit as st
import random

def get_secret_number():
    return random.randint(1, 100)

def initial_state(post_init=False):
    if not post_init:
        st.session_state.input = 0
    st.session_state.number = get_secret_number()
    st.session_state.attempt = 0
    st.session_state.over = False

def restart_game():
    initial_state(post_init=True)
    st.session_state.input += 1

def get_hint(number):
    operation_list = ["+", "-", "*"]
    operation = random.choice(operation_list)
    if operation == "+":
        op1 = random.randint(1, number-1)
        op2 = number-op1
        return f"{op1}+{op2}=?"
    elif operation == "-":
        op1 = random.randint(number+1, 100)
        op2 = op1-number
        return f"{op1}-{op2}=?"
    else:
        for op1 in range(100, 0, -1):
            for op2 in range(1, 101):
                if op1*op2 == number:
                    return f"{op1}*{op2}=?"

def main():
  
    if 'number' not in st.session_state:
        initial_state()

    st.button('New game', on_click=restart_game)

    placeholder, debug, hint_text = st.empty(), st.empty(), st.empty()

    guess = placeholder.number_input(
        f'Enter your guess from 1 - {100}',
        key=st.session_state.input,
        min_value=0,
        max_value=100,
    )

    col1, _, _, _, col2 = st.columns(5)
    with col1:
        hint = st.button('Hint')

    with col2:
        if not guess:
            st.write(f"Attempt Left : 7")
        if guess:
            st.write(f"Attempt Left : {6-st.session_state.attempt}")

    if hint:
        hint_response = get_hint(st.session_state.number)
        hint_text.info(f'{hint_response}')

    if guess:
        if st.session_state.attempt < 6:
            st.session_state.attempt += 1
            if guess < st.session_state.number:
                debug.warning(f'{guess} is too low!')
            elif guess > st.session_state.number:
                debug.warning(f'{guess} is too high!')
            else:
                debug.success(
                    f'Yay! you guessed it right '
                )
                st.balloons()
                st.session_state.over = True
                placeholder.empty()
        else:
            debug.error(
                f'Sorry you Lost! The number was {st.session_state.number}'
            )
            st.session_state.over = True
            placeholder.empty()
            hint_text.empty()

if __name__ == '__main__':
    main()
