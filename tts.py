from os import system


def tts(utterance):
	system('say ' + utterance)