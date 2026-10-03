// Exports the poster's text as two outlined PDFs (giant numeral, everything else).
// Usage: node export-text-layers.js num.pdf rest.pdf, then pdftocairo -svg each, then build_svg.py
const path=require('path');const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for (const [mode,out] of [['num',process.argv[2]],['rest',process.argv[3]]]){
const p=await b.newPage({viewport:{width:1080,height:1350}});
await p.goto('file://'+path.resolve('index.html'));await p.evaluate(()=>document.fonts.ready);
await p.addStyleTag({content:`html,body,.poster{background:transparent!important}.glow,.beams,.scan,.logo{display:none!important}`+(mode==='num'?`.poster>*:not(.num){display:none!important}`:`.num{display:none!important}`)});
await p.pdf({path:out,width:'1080px',height:'1350px',printBackground:true,margin:{top:0,right:0,bottom:0,left:0},pageRanges:'1'});await p.close();}
await b.close();})();
