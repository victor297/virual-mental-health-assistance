import streamlit as st
import random
import base64
import time as tm
from PIL import Image

st.set_page_config(page_title="Sudoku", page_icon="./sudoku_icon.png", layout="wide", initial_sidebar_state="expanded")

# General variables
sample_gm = "921637584674518923583492167269854371745361298138729645856273419412985736397146852"
emoji_lst = {1:'1️⃣', 2:'2️⃣', 3:'3️⃣', 4:'4️⃣', 5:'5️⃣', 6:'6️⃣', 7:'7️⃣', 8:'8️⃣', 9:'9️⃣'}
entry_emoji = "❔"
dlvllst = {"Easy": random.randint(45, 60), "Medium": random.randint(35, 45), "Difficult": random.randint(30, 35)}
vline = f"<hr style='margin-top: 0; margin-bottom: 0; size: 1px; border: 1px dashed; color: #2E7D32;'>"
vrules = """
              <h3>Rules:</h3>
              1: Each row must contain the numbers from 1 to 9, without duplicates.<br>
              2: Each column must contain the numbers from 1 to 9, without duplicates.<br>
              3: The digits can only occur once per 3x3 block.<br>
              """
jumble_options = [
  "hbd 1-2", "hbd 1-3", "hbd 2-3",
  "vbd 1-2", "vbd 1-3", "vbd 2-3",
  "row 1-2", "row 1-3", "row 2-3",
  "row 4-5", "row 4-6", "row 5-6",
  "row 7-8", "row 7-9", "row 8-9",
  "col 1-2", "col 1-3", "col 2-3",
  "col 4-5", "col 4-6", "col 5-6",
  "col 7-8", "col 7-9", "col 8-9",
]

# Session variables
mystate = st.session_state
if "changed_grid_indices" not in mystate: mystate.changed_grid_indices = {}
if "balance_numbers" not in mystate: mystate.balance_numbers = 0
if "grid_indices" not in mystate: mystate.grid_indices = [int(x) for x in sample_gm]
if "starter_func_run_once" not in mystate: mystate.starter_func_run_once = False

def ColSwap(vSrc, vTgt):
  src_st = (vSrc - 1)
  tgt_st = (vTgt - 1)

  for x in range(9):
    mystate.grid_indices[src_st], mystate.grid_indices[tgt_st] = mystate.grid_indices[tgt_st], mystate.grid_indices[src_st]
    src_st = src_st + 9
    tgt_st = tgt_st + 9

def RowSwap(vSrc, vTgt):
  src_nd = (vSrc * 9)
  src_st = (src_nd - 9)
  
  tgt_nd = (vTgt * 9)
  tgt_st = (tgt_nd - 9)

  mystate.grid_indices[src_st:src_nd], mystate.grid_indices[tgt_st:tgt_nd] = mystate.grid_indices[tgt_st:tgt_nd], mystate.grid_indices[src_st:src_nd]

def BandSwap(vType, vOrientation, vSrcTgt):
  if vType == "band":
    if vOrientation == "horizontal":
      if vSrcTgt == "1-2":  # swap hband 1 & 2
        RowSwap(1, 4)   # vSrc, vTgt
        RowSwap(2, 5)   # vSrc, vTgt
        RowSwap(3, 6)   # vSrc, vTgt
      
      if vSrcTgt == "1-3":  # swap hband 1 & 3
        RowSwap(1, 7)   # vSrc, vTgt
        RowSwap(2, 8)   # vSrc, vTgt
        RowSwap(3, 9)   # vSrc, vTgt

      if vSrcTgt == "2-3":  # swap hband 2 & 3
        RowSwap(4, 7)   # vSrc, vTgt
        RowSwap(5, 8)   # vTgt
        RowSwap(6, 9)   # vTgt

    if vOrientation == "vertical":
      if vSrcTgt == "1-2":  # swap hband 1 & 2
        ColSwap(1, 4)   # vSrc, vTgt
        ColSwap(2, 5)   # vSrc, vTgt
        ColSwap(3, 6)   # vSrc, vTgt
      
      if vSrcTgt == "1-3":  # swap hband 1 & 3
        ColSwap(1, 7)   # vSrc, vTgt
        ColSwap(2, 8)   # vSrc, vTgt
        ColSwap(3, 9)   # vSrc, vTgt

      if vSrcTgt == "2-3":  # swap hband 2 & 3
        ColSwap(4, 7)   # vSrc, vTgt
        ColSwap(5, 8)   # vSrc, vTgt
        ColSwap(6, 9)   # vSrc, vTgt

def ShowResponseTable():
  tblhdr = """
            <style>
              table { border-collapse: collapse; font-family: Calibri, sans-serif; }
              colgroup, tbody { border: solid medium; }
              td { border: solid thin; height: 1.4em; width: 1.4em; text-align: center; padding: 0; }
            </style>
              <table>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>

                <tbody>
          """
  tblftr = """
          </tbody>
        </table>
  """

  tbdy = "<tr>"
  for i in range(len(mystate.grid_indices)):
    cell_color = "" if (i+1) in mystate.given_grid_indices else "background-color:#F8BBD0; "
    tbdy = tbdy + f"<td style='{cell_color}'>" + str(mystate.grid_indices[i]) + "</td>"

    if ((i+1) / 9) == int((i+1) / 9) and i != 0: tbdy = tbdy + "</tr><tr>"

  ohtml = "<center>" + tblhdr + tbdy + tblftr + "</center>"
  with st.popover("Show Solved Sudoku Puzzle", use_container_width=True): st.html(ohtml)

def GenerateGivenList(dlvl):
  start, end, num_random_numbers = 1, 81, dlvllst[dlvl]
  random_numbers = []
  while len(random_numbers) < num_random_numbers:
    rndmno = random.randint(start, end)
    if rndmno not in random_numbers: random_numbers.append(rndmno)
  
  mystate.balance_numbers = 81 - dlvllst[dlvl]

  return random_numbers

def ReadPictureFile(wch_fl):
  try:
    pxfl = f"./{wch_fl}"
    return base64.b64encode(open(pxfl, 'rb').read()).decode()

  except: return ""

def BtnCallback2(ptr, btn_no):
  ptr = ptr + 1
  mystate.changed_grid_indices[ptr] = btn_no
  mystate.balance_numbers = mystate.balance_numbers + 1 if btn_no == 0 else mystate.balance_numbers - 1
  if mystate.balance_numbers < 0: mystate.balance_numbers = 0

@st.experimental_dialog("Select a number", width="small")
def BtnCallback(ptr):
    sc1, sc2, sc3, sc4, sc5 = st.columns(5)
    sc1.button(entry_emoji, key="cb0", on_click=BtnCallback2, args=(ptr, 0))
    sc2.button('1️⃣', key="cb1", on_click=BtnCallback2, args=(ptr, 1))
    sc3.button('2️⃣', key="cb2", on_click=BtnCallback2, args=(ptr, 2))
    sc4.button('3️⃣', key="cb3", on_click=BtnCallback2, args=(ptr, 3))
    sc5.button('4️⃣', key="cb4", on_click=BtnCallback2, args=(ptr, 4))
    sc1.button('5️⃣', key="cb5", on_click=BtnCallback2, args=(ptr, 5))
    sc2.button('6️⃣', key="cb6", on_click=BtnCallback2, args=(ptr, 6))
    sc3.button('7️⃣', key="cb7", on_click=BtnCallback2, args=(ptr, 7))
    sc4.button('8️⃣', key="cb8", on_click=BtnCallback2, args=(ptr, 8))
    sc5.button('9️⃣', key="cb9", on_click=BtnCallback2, args=(ptr, 9))

def DisplayGame():
  tblhdr = """
            <style>
              table { border-collapse: collapse; font-family: Calibri, sans-serif; }
              colgroup, tbody { border: solid medium; }
              td { border: solid thin; height: 1.4em; width: 1.4em; text-align: center; padding: 0; }
            </style>
              <table>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>
                <colgroup><col><col><col></colgroup>

                <tbody>
          """
  tblftr = """
          </tbody>
        </table>
  """

  tbdy = "<tr>"
  for i in range(len(mystate.grid_indices)):
    idxno = (i+1)
    td_bgcolor = ""
    td_contents = entry_emoji
    if idxno in mystate.given_grid_indices:
      td_bgcolor = "background-color:yellow;"
      td_contents = str(mystate.grid_indices[i])

    tbdy = tbdy + f"<td style='{td_bgcolor} cursor: pointer;' onClick='streamlitSendMessage({idxno})'>" + td_contents + "</td>"
    
    if idxno in mystate.changed_grid_indices.keys():
      tbdy = tbdy.replace(entry_emoji, emoji_lst[mystate.changed_grid_indices[idxno]])

    if ((i+1) / 9) == int((i+1) / 9) and i != 0: tbdy = tbdy + "</tr><tr>"

  ohtml = "<center>" + tblhdr + tbdy + tblftr + "</center>"
  with st.expander("🧩 Sudoku Grid", expanded=True): st.html(ohtml)

def ShowScratchpad():
  scratchpad = "‣ Scratchpad for numbers you may use in the grid."
  with st.expander("✏️ Scratchpad"):
    st.text_area("Use this space to write down potential numbers", value=scratchpad, height=200)

def StarterFunctionRunOnce():
    active_option = random.choice(jumble_options)
    jumble_cmd, jumble_st, jumble_nd = active_option[0:3], int(active_option[4]), int(active_option[6])

    if jumble_cmd == "row":
        RowSwap(jumble_st, jumble_nd)
    elif jumble_cmd == "col":
        ColSwap(jumble_st, jumble_nd)
    elif jumble_cmd == "hbd":
        BandSwap("band", "horizontal", f"{jumble_st}-{jumble_nd}")
    elif jumble_cmd == "vbd":
        BandSwap("band", "vertical", f"{jumble_st}-{jumble_nd}")

    # Set the given grid indices for the selected difficulty level
    mystate.given_grid_indices = GenerateGivenList(st.session_state.difficulty)

    # Ensure the function only runs once
    mystate.starter_func_run_once = True

# Initialize the game on first load or when the difficulty level is changed
if not mystate.starter_func_run_once:
    mystate.starter_func_run_once = True
    mystate.difficulty = st.selectbox("Select Difficulty Level", list(dlvllst.keys()))
    StarterFunctionRunOnce()

# Display the game grid
DisplayGame()

# Display the scratchpad
ShowScratchpad()

# Button to show the solved puzzle
if st.button("Show Solved Sudoku Puzzle"):
    ShowResponseTable()

# Display rules
st.markdown(vrules, unsafe_allow_html=True)
