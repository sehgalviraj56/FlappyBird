import os
import pygame

# Mixer Initialize
sound_enabled = False
SND_BEEP = None
SND_DIE = None
SND_CLICK = None

try:
    pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
    
    # MP3 Files Loader (Agar kisi file ka naam alag ho toh bas text change kar lena)
    if os.path.exists("beep.mp3"): 
        SND_BEEP = pygame.mixer.Sound("beep.mp3")
    if os.path.exists("die.mp3"): 
        SND_DIE = pygame.mixer.Sound("die.mp3")
    if os.path.exists("click.mp3"): 
        SND_CLICK = pygame.mixer.Sound("click.mp3")
        
    sound_enabled = True
except Exception as e:
    print(f"Sound initialization error: {e}")
    sound_enabled = False

def play_beep():
    if sound_enabled and SND_BEEP:
        try:
            SND_BEEP.play()
        except:
            pass

def play_die():
    if sound_enabled and SND_DIE:
        try:
            SND_DIE.play()
        except:
            pass

def play_click():
    if sound_enabled and SND_CLICK:
        try:
            SND_CLICK.play()
        except:
            pass
