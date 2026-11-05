#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Iconicity rating task - PILOT
Layout modelled on Winter et al.'s online iconicity rating task
(1-7 scale + "Skip" if the word is unknown), with a definition
shown under each word.

Stimuli are read from stimuli.csv (columns: word, definition).
Data are saved to the data/ folder as one CSV per participant.
Press ESC at any time to quit (data collected so far are saved).
"""

from psychopy import visual, core, event, data, gui
import os
import random

# ---------------- settings you may want to tweak ----------------
STIM_FILE = 'stimuli.csv'
FULLSCREEN = True
CLICK_TO_ADVANCE = False   # True = clicking a rating moves on (like the original);
                          # False = participant must click "Next" (lets them change their mind)
BG_COLOR = 'white'
TEXT_COLOR = 'black'
# -----------------------------------------------------------------

# ---Consent form--- 

consent = gui.Dlg(
    title='Study information',
    labelButtonOK='OK',
    labelButtonCancel='Cancel' # button for declining to participate. 
)

consent.addText(
    'Iconicity study\n\n'
 
    'INTRODUCTION\n'
    'You are being invited to take part in a research study. Please read this\n'
    'information carefully before deciding whether to participate. The study\n'
    'investigates how people rate words on an iconicity scale.\n'
    'You can take part if you are at least 18 years old and if English\n'
    'is your second language.\n\n'
 
    'If you have any questions regarding the study, feel free to contact the\n'
    'primary investigators:\n'
    'Paula Rits, paula.rits@gmail.com\n' 
    'Emilie Engelbrechtsen, emilieschacke@gmail.com\n\n'
 
    'PURPOSE OF THE RESEARCH\n'
    'This study is conducted as part of the Cognition and Communication\n'
    'final exam in the first semester of Cognitive Science.\n\n'
 
    'STUDY PROCEDURE\n'
    'You will be asked to rate the iconicity of 60 words in the English language.\n'
    'More elaborate instructions will be provided after consenting.\n'
    'The study takes around 10 minutes. It is possible to stop at any time,\n'
    'without giving a reason, by pressing Escape.\n\n'
 
    'BENEFITS AND RISKS\n'
    'There are no risks other than those you meet in daily life.\n\n'
 
    'CONFIDENTIALITY AND DATA HANDLING\n'
    'We record only your age, gender and your answers under a\n'
    'randomly generated participant ID. The data are anonymous,\n'
    'are stored securely by the researchers for 1 year, and may\n'
    'be shared in anonymised form for research purposes. Because the data are\n'
    'anonymous, they cannot be identified and withdrawn after data collection\n'
    'has ended.\n\n'
 
    'SIGNATURE AND DATE\n'
    'By clicking OK, I confirm that I understand the information above and that\n'
    'I give my consent to participate in the research and for my data to be used\n'
    'as described in this document. Click Cancel if you do not wish to take part.')
    
consent.show()

# quit experiment if participant withdraws consent. 
if not consent.OK:
    core.quit()

# ---Participant---
box = gui.Dlg(title='Experiment on Iconicity')
box.addField('Age')
box.addField('Gender', choices=['Female', 'Male', 'Other'])
box.addField('Is English your second language?', choices=['Yes', 'No'])
answers = box.show()

# Pressed Cancel -> quit
if not box.OK:
    core.quit()
    
age_text = answers['Age']
gender = answers['Gender']
secondlang = answers['Is English your second language?']

# Age must be a whole number
try:
    age = int(age_text)
except ValueError:
    age = 0  # treat invalid input as not eligible (because the cutoff is 18 and over)

# Eligibility check: 18+ and English as a second language
if age < 18 or secondlang == 'No':
    msg = gui.Dlg(title='Experiment on Iconicity')
    msg.addText('Thank you for your interest!\n\n'
                'Unfortunately you do not meet the criteria for this study.')
    msg.show()
    core.quit()  # quit without saving anything
    
participant = f'P{random.randint(10000, 99999)}'

# --- Logfile settings ---
    
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# participant = data.getDateStr()   # placeholder ID until the dialog box is added
os.makedirs('data', exist_ok=True)
filename = os.path.join('data', f'iconicity_pilot_{participant}')

exp = data.ExperimentHandler(name='iconicity_pilot',
                             extraInfo={'participant': participant},
                             dataFileName=filename,
                             savePickle=False, saveWideText=True)


win = visual.Window(fullscr=FULLSCREEN, size=(1280, 800), color=BG_COLOR,
                    units='height', allowGUI=True)
mouse = event.Mouse(win=win)

# ---------------- stimuli on screen ----------------
counter_txt = visual.TextStim(win, text='', pos=(0, 0.42), height=0.025,
                              color=TEXT_COLOR)
word_txt = visual.TextStim(win, text='', pos=(0, 0.17), height=0.08,
                           bold=True, color=TEXT_COLOR)
definition_txt = visual.TextStim(win, text='', pos=(0, 0.06), height=0.048,
                                 wrapWidth=1.1, italic=True, color='#555555')

scale_labels = ['(1) Not iconic at all', '(2)', '(3)', '(4)', '(5)', '(6)',
                '(7) Very iconic']
slider = visual.Slider(win, ticks=(1, 2, 3, 4, 5, 6, 7), labels=scale_labels,
                       granularity=1, style='radio', size=(1.2, 0.02),
                       pos=(0, -0.08), labelHeight=0.02, color=TEXT_COLOR,
                       markerColor='#2a6fdb', lineColor='#bbbbbb',
                       labelColor=TEXT_COLOR)

skip_info = visual.TextStim(win, pos=(0, -0.24), height=0.025, color=TEXT_COLOR,
                            text="I am not familiar with this word")
skip_box = visual.Rect(win, width=0.22, height=0.05, pos=(0, -0.31),
                       lineColor='#999999', fillColor='white')
skip_label = visual.TextStim(win, text='Skip', pos=(0, -0.31), height=0.022,
                             color=TEXT_COLOR)

next_box = visual.Rect(win, width=0.22, height=0.05, pos=(0, -0.42),
                       lineColor='#2a6fdb', fillColor='#2a6fdb')
next_label = visual.TextStim(win, text='Next', pos=(0, -0.42), height=0.022,
                             color='white')

# ---------------- helpers ----------------
def check_quit():
    if event.getKeys(['escape']):
        exp.saveAsWideText(filename + '.csv', delim=',')
        win.close()
        core.quit()


def wait_mouse_release():
    """Prevent a click from carrying over into the next screen."""
    while any(mouse.getPressed()):
        check_quit()
        core.wait(0.01)
    mouse.clickReset()


def show_text_screen(text, key='space'):
    msg = visual.TextStim(win, text=text, height=0.03, wrapWidth=1.2,
                          color=TEXT_COLOR)
    event.clearEvents()
    while True:
        msg.draw()
        win.flip()
        keys = event.getKeys([key, 'escape'])
        if 'escape' in keys:
            check_quit()
            win.close(); core.quit()
        if key in keys:
            break


# ---------------- instructions ----------------
instructions = (
    "Iconicity is the relationship between the form and the meaning of a word. "
    "In simple terms, iconic words feel, sound or look like what they mean: "
    "“boom” sounds like an explosion, “stutter” resembles stuttering itself, "
    "saying “large” makes your mouth open wide, and “teeny-weeny” does the "
    "opposite. These words have high iconicity ratings.\n"
    "“Justice”, “the” and “shape”, on the other hand, are hard to imagine "
    "based on the word alone and don't sound like what they mean.\n\n"
    "In this study you will see English words, each followed by a short "
    "definition. For each word, rate its iconicity from 1 (not iconic at all) "
    "to 7 (very iconic).\n\n"
    "There are no right or wrong answers! Read each definition carefully, "
    "as some words appear more than once with different definitions.\n\n"
    "If you don't know a word or don't feel comfortable rating it, "
    "click “Skip”.\n\n"
    "Press SPACE to begin."
)
show_text_screen(instructions)

# ---------------- trials ----------------
conditions = data.importConditions(STIM_FILE)
trials = data.TrialHandler(trialList=conditions, nReps=1, method='random')
exp.addLoop(trials)
n_trials = len(conditions)
rt_clock = core.Clock()

for i, trial in enumerate(trials):
    counter_txt.text = f'Trial {i + 1} of {n_trials}'
    word_txt.text = trial['word']
    definition_txt.text = trial['definition']
    slider.reset()
    wait_mouse_release()
    event.clearEvents()

    rating, skipped, rt = None, False, None
    rt_clock.reset()

    while True:
        for stim in (counter_txt, word_txt, definition_txt,
                     slider, skip_info, skip_box, skip_label):
            stim.draw()
        rated = slider.getRating() is not None
        if rated and not CLICK_TO_ADVANCE:
            next_box.draw(); next_label.draw()
        win.flip()

        if mouse.isPressedIn(skip_box):
            skipped, rt = True, rt_clock.getTime()
            break
        if rated and CLICK_TO_ADVANCE:
            rating, rt = slider.getRating(), slider.getRT()
            break
        if rated and not CLICK_TO_ADVANCE and mouse.isPressedIn(next_box):
            rating, rt = slider.getRating(), rt_clock.getTime()
            break
        check_quit()

    exp.addData('trial_num', i + 1)
    exp.addData('rating', rating)
    exp.addData('skipped', skipped)
    exp.addData('rt', rt)
    exp.nextEntry()

# ---------------- end ----------------
exp.saveAsWideText(filename + '.csv', delim=',')
show_text_screen("Thank you! You have finished the pilot.\n\nPress SPACE to exit.")
win.close()
core.quit()