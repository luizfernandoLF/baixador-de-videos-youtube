import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import font
from tkinter import messagebox

def btn_baixar_video_audio():
    janela_baixar_video_audio = tk.Toplevel(janela_principal)
    janela_baixar_video_audio.config(padx=20,pady=20)

    janela_baixar_video_audio.grab_set()

    #caixa de texto pra colar o link do video
    label_link_video = tk.Label(janela_baixar_video_audio, text="Cole o link do vídeo do YouTube")
    label_link_video.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_link_video = tk.Entry(janela_baixar_video_audio, width=60)
    entry_link_video.grid(row=0, column=1, padx=5, pady=5)

    #caixa de texto pra setar o caminho onde o video vai ser baixado
    label_path = tk.Label(janela_baixar_video_audio, text="Cole aqui o caminho da pasta onde você quer que o download seja feito")
    label_path.grid(row=1, column=0, padx=5,pady=5, sticky="w")
    entry_path = tk.Entry(janela_baixar_video_audio, width=60)
    entry_path.grid(row=1, column=1, padx=5, pady=5)


    def btn_baixar():
        url = entry_link_video.get()
        path = entry_path.get()
        url = url.strip()
        path = path.strip()

        # validação básica dos campos
        if not url or not path:
            messagebox.showerror("Erro", "Obrigatório URL/Link do vídeo e caminho da pasta onde o vídeo será salvo")
            return

        # normaliza o caminho e cria a pasta se necessário
        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar/usar o diretório: {e}")
            return

        # Criar label para mensagem de status
        status_label = tk.Label(janela_baixar_video_audio, text="Download em progresso...")
        status_label.grid(row=3, column=1, pady=5)

        # monta o template de saída para o yt_dlp
        outtmpl = os.path.join(path, '%(title)s.%(ext)s')

        try:
            options = {
                'format': 'bestvideo+bestaudio/best',  # Baixa vídeo na melhor qualidade disponível
                'outtmpl': outtmpl
            }
            janela_baixar_video_audio.update()  # Atualiza a janela para mostrar a mensagem, pq o tkinter bloqueia a tela até que  o download termine
            with YoutubeDL(options) as ydl:
                ydl.download([url])
            status_label.config(text="Download concluído!") #atualiza a label status_label que antes mostrava "Download em progresso" pra essa nova mensagem do text
            messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso!") #mostra um pop up dizendo que o video foi baixado com sucesso, o primeiro parâmetro é o título da janela, o segundo é a mensagem
        except Exception as e:
            status_label.config(text="Erro no download!")
            messagebox.showerror("Erro ao baixar", str(e))

    #esse botão tem que tá dentro da função principal btn_baixar_video_audio
    btn_salvar = tk.Button(janela_baixar_video_audio, text="Salvar", command=btn_baixar, width=30)
    btn_salvar.grid(row=2, column=1, padx=10, pady=10)




janela_principal = tk.Tk()
janela_principal.title("Baixador de vídeos do YouTube")
janela_principal.config(padx=200, pady=200)    

fonte = font.Font(family="Times New Roman", size=22, weight="bold")
fonte_botoes = font.Font(family="Times New Roman", size=12)

#titulo da janela
label_titulo = tk.Label(
    janela_principal,
    text="Bem vindo ao baixador de vídeo, escolha uma das opções",
    font=fonte
)
label_titulo.pack(pady=20)

#criar botões
btn_baixar_video = tk.Button(janela_principal,
                             text="Baixar vídeo e áudio",
                             width=30,
                             height=2,
                             font=fonte_botoes,
                            command=btn_baixar_video_audio
                             )
btn_baixar_video.pack(pady=5)


btn_baixar_audio = tk.Button(janela_principal,
                             text="Baixar apenas áudio",
                             width=30,
                             height=2,
                             font=fonte_botoes
                            #  command=
                             )
btn_baixar_audio.pack(pady=5)












janela_principal.mainloop()