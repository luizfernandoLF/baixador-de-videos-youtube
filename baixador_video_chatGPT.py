import os
from yt_dlp import YoutubeDL

def download_video(url):
    options = {
        'format': 'bestvideo+bestaudio/best',  # Baixa vídeo na melhor qualidade disponível
        'outtmpl': 'downloads/%(title)s.%(ext)s'  # Salva na pasta downloads
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    print("Vídeo baixado com sucesso!")

def download_audio(url):
    options = {
        'format': 'bestaudio/best',  # Baixa apenas o áudio
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Extrai áudio
            'preferredcodec': 'mp3',  # Converte para MP3
            'preferredquality': '192',  # Define a qualidade do áudio
        }]
    }
    with YoutubeDL(options) as ydl:
        ydl.download([url])
    print("Áudio baixado e convertido para MP3 com sucesso!")

def main():
    url = input("Digite o link do vídeo ou música: ")
    print("O que deseja baixar?")
    print("1. Vídeo (formato MP4)")
    print("2. Áudio (formato MP3)")
    
    choice = input("Escolha (1/2): ")
    if choice == "1":
        download_video(url)
    elif choice == "2":
        download_audio(url)
    else:
        print("Opção inválida!")

if __name__ == "__main__":
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    main()
