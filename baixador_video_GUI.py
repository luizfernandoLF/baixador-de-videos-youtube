import os
from yt_dlp import YoutubeDL
import tkinter as tk
from tkinter import font
from tkinter import messagebox
import webbrowser
import threading
# Usamos threads para executar downloads em segundo plano sem bloquear a GUI.
# O Tkinter processa eventos (cliques, redraws) na thread principal; se um
# download rodar nessa mesma thread a janela ficará 'congelada' e o sistema
# pode marcar o programa como "Não está respondendo". Por isso iniciamos
# operações de I/O longas em threads separadas e usamos `after()` para
# atualizar widgets com segurança a partir da thread principal.

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

        def download_thread():
            # Função que será executada em uma thread separada para
            # não bloquear o loop de eventos do Tkinter.
            try:
                # Monta as opções do yt_dlp:
                # - 'format' define a qualidade/fluxo a ser baixado
                # - 'outtmpl' informa o caminho/arquivo de saída (usa o outtmpl
                #    construído a partir do entry_path do usuário)
                options = {
                    'format': 'bestvideo+bestaudio/best',  # Baixa vídeo na melhor qualidade disponível
                    'outtmpl': outtmpl
                }
                # Abre o gerenciador do yt_dlp e executa o download. Esta
                # chamada faz I/O e pode demorar bastante, por isso está
                # dentro da thread (evita travar a GUI).
                with YoutubeDL(options) as ydl:
                    ydl.download([url])

                janela_baixar_video_audio.after(0, lambda: status_label.config(text="Download concluído!"))
                janela_baixar_video_audio.after(0, lambda: messagebox.showinfo("Sucesso", "Vídeo baixado com sucesso!"))
            except Exception as e:
                # Se ocorrer erro durante o download, também atualizamos a
                # GUI pela thread principal usando `after` para mostrar o
                # status de erro e o popup com a mensagem.
                janela_baixar_video_audio.after(0, lambda: status_label.config(text="Erro no download!"))
                janela_baixar_video_audio.after(0, lambda: messagebox.showerror("Erro ao baixar", str(e)))

        janela_baixar_video_audio.update()  # Atualiza a janela para mostrar a mensagem inicial
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()

    #esse botão tem que tá dentro da função principal btn_baixar_video_audio
    btn_salvar = tk.Button(janela_baixar_video_audio, text="Salvar", command=btn_baixar, width=30)
    btn_salvar.grid(row=2, column=1, padx=10, pady=10)

def baixar_audio():
    janela_baixar_audio = tk.Toplevel(janela_principal)
    janela_baixar_audio.grab_set()

    label_link_video = tk.Label(janela_baixar_audio, text="Cole o link do vídeo do YouTube")
    label_link_video.grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_link_video = tk.Entry(janela_baixar_audio, width=60)
    entry_link_video.grid(row=0, column=1, padx=5, pady=5)

    # caixa de texto pra setar o caminho onde o audio vai ser baixado
    label_path = tk.Label(janela_baixar_audio, text="Cole aqui o caminho da pasta onde você quer que o download seja feito")
    label_path.grid(row=1, column=0, padx=5,pady=5, sticky="w")
    entry_path = tk.Entry(janela_baixar_audio, width=60)
    entry_path.grid(row=1, column=1, padx=5, pady=5)

    def btn_baixar():
        url = entry_link_video.get().strip()
        path = entry_path.get().strip()

        if not url or not path:
            messagebox.showerror("Erro", "Obrigatório URL/Link do vídeo e caminho da pasta onde o áudio será salvo")
            return

        path = os.path.expanduser(path)
        path = os.path.abspath(path)
        try:
            os.makedirs(path, exist_ok=True)
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar/usar o diretório: {e}")
            return

        status_label = tk.Label(janela_baixar_audio, text="Download em progresso...")
        status_label.grid(row=3, column=1, pady=5)

        outtmpl = os.path.join(path, '%(title)s.%(ext)s')

        def download_thread():
            # Função executada em thread separada para evitar bloqueio da GUI.
            try:
                # Monta as opções do yt_dlp para baixar apenas o áudio e depois
                # converter/extrair para MP3 com o FFmpeg (postprocessor).
                # Usamos `outtmpl` criado a partir do `entry_path` para garantir
                # que o arquivo final seja salvo na pasta escolhida pelo usuário.
                options = {
                    'format': 'bestaudio/best',
                    'outtmpl': outtmpl,
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }]
                }
                # Executa o download/extração — operação de I/O que pode ser
                # demorada, por isso está na thread separada.
                with YoutubeDL(options) as ydl:
                    ydl.download([url])

                # Atualiza a GUI pela thread principal (seguro) informando
                # que o download acabou e mostrando um popup de sucesso.
                janela_baixar_audio.after(0, lambda: status_label.config(text="Download concluído!"))
                janela_baixar_audio.after(0, lambda: messagebox.showinfo("Sucesso", "Áudio baixado com sucesso!"))
            except Exception as e:
                # Em caso de erro agendamos a atualização da GUI para mostrar
                # o estado de erro e a mensagem de exceção.
                janela_baixar_audio.after(0, lambda: status_label.config(text="Erro no download!"))
                janela_baixar_audio.after(0, lambda: messagebox.showerror("Erro ao baixar", str(e)))

        janela_baixar_audio.update()
        thread = threading.Thread(target=download_thread, daemon=True)
        thread.start()

    btn_salvar = tk.Button(janela_baixar_audio, text="Salvar", command=btn_baixar, width=30)
    btn_salvar.grid(row=2, column=1, padx=10, pady=10)


janela_principal = tk.Tk()
janela_principal.title("Baixador de vídeos do YouTube")
# janela_principal.config(padx=200, pady=200)    
janela_principal.geometry("800x600+100+50")    

fonte = font.Font(family="Times New Roman", size=22, weight="bold")
fonte_botoes = font.Font(family="Times New Roman", size=12)

#titulo da janela
label_titulo = tk.Label(
    janela_principal,
    text="Bem vindo ao baixador de vídeo, escolha uma das opções",
    font=fonte
)
label_titulo.pack(pady=100)

#criar botões
btn_baixar_video = tk.Button(janela_principal,
                             text="Baixar vídeo com áudio",
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
                             font=fonte_botoes,
                             command=baixar_audio
                             )
btn_baixar_audio.pack(pady=5)




# footer_frame = tk.Frame(janela_principal, bg="lightgray", height=80)
# # Posiciona o frame na parte inferior e expande horizontalmente
# footer_frame.pack(side="bottom", fill="x")

# status_label = tk.Label(footer_frame, text="" \
# "Criado por Luiz Fernando\n Projeto ainda em desenvolvimento\nSe quiser contribuir, eis o GitHub: https://github.com/luizfernandoLF/baixador-de-videos-youtube",
# bg="lightgray", anchor="w")
# # Posiciona a label no frame do rodapé, alinhando à esquerda (west)
# status_label.pack(side="left", padx=10, pady=5)



janela_principal.mainloop()