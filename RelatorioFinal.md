Projeto Final - Processamento de Imagem

Nome: Samuel Ferreira Guimarães Santos - 9293498

Descrição do Problema

O objetivo do projeto é transformar uma imagem que contém um programa em código usando OCR (Optical Character Recognition), que é uma tecnologia para reconhecer caracteres a partir de um arquivo de imagem. Os códigos serão obtidos do site www.codeforces.com, onde ocorrem competições no estilo maratona de programação. 	Nessas competições, uma parte da pontuação é obtida criando casos de teste para "quebrar" a solução de outros participantes. Se o caso criado, "quebrar" a solução do adversário, é concedida uma pontuação; caso contrário, o competidor que enviou o caso, perde pontos. A plataforma permite acesso ao código dos outros competidores no formato de imagem, por isso, testar o caso localmente demanda muito tempo, pois é necessário copiar o código inteiro. O projeto seria utilizado para acelerar esse processo, pois seria possível testar o caso localmente com um tempo consideravelmente menor.

Solução

Para a implementação do projeto foi utilizado a biblioteca Tesseract, da Google, de OCR e a biblioteca OpenCv par Python.
Primeiro passo, do projeto foi capturar uma imagem e fazer o reconhecimento do texto, usando o Tesseract.

| Código | Texto Reconhecido |
|-------------|--------------|
|<img src="images/sample2.png">|Texto reconhecido:<br>mam: Gunman<br>mum: «at»<br>uslng namsvate 5m;<br>m lam” (<br>m<br>(111))”<br>markstnnq. m) In;<br>mom rB' 14:; m) ( <br> mm; 5; <br>Ms!»<br>)<br>mom ;<br>smug s;<br>wlsl<br>- 14:: m) (<br>)  <br>m m <br>fuﬂnalkstnny. 1n!) .. : up)<br>”u. mun-1 ) aw<br>m K n.5unnd;<br>(“mm <br>return |


 Como pode ser observado, os resultados iniciais foram ruins. Para melhorar os resultados, foram utilizadas algumas técnicas aprendidas em aula, a fim de processar a imagem. 
	Como as cores da sintaxe não fazem diferença no código, a imagem foi convertida para escala de cinza. Depois disso, a primeira técnica de realce implementada foi a de equalização de histogramas, porém o resultado não foi satisfatório.
	
| Código | Texto Reconhecido |
|-------------|--------------|
|<img src="images/equalization.png" width="300px" height="450px">|Texto reconhecido: <br>ﬁnctuda dust“<br>ﬁncmle up: . .<br>using namespaue std:<br>int: “in“ {<br>int: ll:<br>aim-:11:<br>lap-astring.1nt=- In:<br>fnr{1liti1-D.1¢ll: 14+] {<br>string 5:-<br>ﬁlm-s:<br>} illl‘lis‘lH:<br>forﬂnté 1-D: 1d]: 14+! {<br>string SF:<br>aim-s:<br>} natal-:4<br>int; tut - D:<br>forwair-astdm int:- p 1:. qr]<br>1ﬂp.second\ =- I)<br>hit +- p. salami:<br>ﬂout-«tut:<br>rah]m' D:<br>}<br>|

Após isso, foi utilizado a função fastNlMeansDenoising do OpenCv para remover os ruídos das imagens utilizando uma média não local. Como pode ser observado abaixo, os poucos caractereces da imagem são realmente reconhecidos.

| Código | Texto Reconhecido |
|-------------|--------------|
|<img src="images/denoising.png" width="250px" height="400px">|“mum. dusxmn<br>“mm. «In.<br>mm nllrslalne m:<br>in: mm) (<br>m: u:<br>um:<br>npsnnm. m: In:<br>mum in 14:; 1+.) (<br>) lama.<br>mum in 14:; 1+.) (<br>)<br>m: m .<br>hull-Insulin. up u I.»<br>"(p.nmm > )|

Depois de alguns testes e pesquisas de transformações, foi possível obter um resultado mais próximo do código esperado, usando as seguintes operações:
  - Aumentar o tamanho da imagem, utilizando a função resize da biblioteca openCV, utlizando a interpolação cúbica
  - Remoção de ruídos para suavizar a imagem
  - Transformação morfológica de erosão.
  
| Código | Texto Reconhecido |
|-------------|--------------|
|<img src="images_output/sample2.png" width="300px" height="500px">|#include <iostream><br>#include <map><br>using namespace std;<br>int main() {<br>int N;<br>cin>>N:<br>nap<string. int> mp:<br>for(int i=0; i<N; i++) {<br>string 5;<br>cin>>s:<br>mp[s]++;<br>}<br>for(int i=0; i<N; i++) {<br>string 5;<br>cin>>s:<br>mp[s]--;<br>}<br>int tot = 0;<br>for(pair<string. int> p : mp)<br>if(p.second > 0)<br>tot += p.second:<br>cout<<tot;<br>return 0:<br>|

Resultados

Com o processamento das imagens, foi possível obter um resultado muito próximo do esperado. O programa ainda erra alguns caracteres, por exemplo, troca de s por 5, de vírgula por ponto-vírgula, de 0 por 6, são os principais erros. Mas na maioria dos casos, funciona muito bem, foi calculado cerca de 95% de acerto dos caracteres.
No futuro, esses casos que possuem maior incidência de erros, poderiam ser tratados separadamente para diminuir a quantidade  de erros, além de estudar outras métodos para pré-processar a imagem antes de rodar o Tesseract
