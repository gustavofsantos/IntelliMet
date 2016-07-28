Este projeto contém um baixador de imagens do INMET.

Exemplo de uso:
===

$ ./get_images.py n_imagens 3 modo vapor

[*] Modo batch
[*] Downloader de imagens do INMET. v0.72
[*] Autor: Gustavo Fernandes dos Santos
[*] Email: gfdsantos@inf.ufpel.edu.br
    -----------------------------------
[!] Imagens são produto do GOES - América Latina - Topo das nuvens
                                                   Visível
                                                   Infravermelho termal
                                                   Vapor d'Agua
    -----------------------------------
[!] Estabelecendo conexao...
[+] Online
[+] Gerando links...
[!] Testando o link:
    
http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607272000.jpg
[+] Link ok.
[!] Testando o link:
    
http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607271930.jpg
[+] Link ok.
[!] Testando o link:
    
http://www.inmet.gov.br/projetos/cga/capre/sepra/GEO/GOES12/AMERICA_SUL/AS12_VA201607271900.jpg
[+] Link ok.
[+] Baixando imagens...

AS12_VA201607272000.jpg 100%[==========================================>] 120,63K   129KB/s    in 0,9s
AS12_VA201607271930.jpg 100%[==========================================>] 120,03K   124KB/s    in 1,0s
AS12_VA201607271900.jpg 100%[==========================================>] 119,16K   148KB/s    in 0,8s    
[!] Tentando criar o diretório "imagens"
[!] O diretório já existe.
[!] Movendo imagens...
[+] Ok.
[+] Pronto.
