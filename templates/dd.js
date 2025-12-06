var myVAR='txt';

const myButton = document.getElementById("botIMG");
  myButton.addEventListener("click", chosedIMAGE());
  const myButton1 = document.getElementById("botTEXT");
  myButton1.addEventListener("click", chosedTEXT());

    function chosedIMAGE(){ myVAR='img'; console.log('tmg');console.log('here is your var: '+myVAR);}
    function chosedTEXT(){myVAR='txt';console.log('txt');console.log('here is your var: '+myVAR);}