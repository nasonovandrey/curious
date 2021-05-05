import numpy as np
import math
import wave
from collections import deque
from random import random
import pygame
import time
import os


CD_RATE = 44100
INT_SIZE = 32767
minor_pentatonic_scale = { 'C4':261.6, 'E-flat':311.1, 'F':349.2, 'G':392.0, 'B-flat':466.2 }


def generate_note(frequency, duration, attenuation):
    sample_rate = CD_RATE
    sample_size = int(sample_rate*duration)

    # initializing ring buffer
    buffer_size = int(sample_rate/frequency)
    ring_buffer = deque([random()-0.5 for i in range(buffer_size)])
    samples = np.array([0]*sample_size, 'float32')

    # Karplus-Strong algorithm
    for i in range(sample_size):
        samples[i] = ring_buffer[0]
        avg = attenuation*0.5*(ring_buffer[0]+ring_buffer[1])
        ring_buffer.append(avg)
        ring_buffer.popleft()

    samples = np.array(samples*INT_SIZE, 'int16')
    return samples.tostring()


def write_wav_file(filename, data):
    f = wave.open(filename, 'wb')
    channels_number = 1
    sample_width = 2
    frame_rate = CD_RATE

    # setting write parameters
    # (nFrames param is set to factual value anyway)
    f.setparams((channels_number, sample_width, frame_rate, frame_rate, 'NONE', 'uncompressed'))
    f.writeframes(data)
    f.close()


class NotePlayer:
    def __init__(self, notes):
        pygame.mixer.pre_init(44100, -16, 1, 2048)
        pygame.init()
        self.note_samples = {}
        for key,value in notes.items():
            write_wav_file(key+'.wav', generate_note(value, 2, 0.996))
            self.note_samples[key] = pygame.mixer.Sound(key+'.wav')

    def play(self, note, delay):
        self.note_samples[note].play()
        time.sleep(delay)

    def play_notes(self, notes, delay=1.5):
        for note in notes:
            self.play(note, delay)

    def clean(self):
        for key in self.note_samples:
            os.remove(key+'.wav')
        

if __name__=='__main__':
    player = NotePlayer(minor_pentatonic_scale)
    notes = input('Print notes from minor pentatonic scale: {scale}\n'.format(scale=','.join(minor_pentatonic_scale)))
    player.play_notes(notes.split(' '), 0.8)
    player.clean()

