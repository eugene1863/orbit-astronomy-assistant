function astronomyAnswer(question) {
 const q=question.toLowerCase().replace(/[^a-z0-9 ]/g,' ').trim().replace(/\s+/g,' ');
 if(['hi','hello','hey'].includes(q))return {answer:"Hello! Ask me about black holes, stars, galaxies, planets, the Moon, light-years, exoplanets, dark matter, or supernovae.",sources:[]};
 if(q.split(' ').some(w=>['latest','today','current','tonight'].includes(w)))return {answer:"I don't have live astronomy news or observing conditions. Try a general astronomy question, or consult a current astronomy source.",sources:[]};
 const ranked=TOPICS.map(([title,aliases,body,url])=>({title,body,url,score:Math.max(0,...aliases.filter(a=>(' '+q+' ').includes(' '+a+' ')).map(a=>a.split(' ').length*10+a.length))})).filter(r=>r.score>0).sort((a,b)=>b.score-a.score||b.title.localeCompare(a.title));
 if(!ranked.length)return {answer:"I don't have a reliable answer in my small reference set yet. Try asking what a black hole is, how stars form, or about galaxy shapes.",sources:[]};
 const selected=ranked.slice(0,q.split(' ').some(w=>['compare','difference'].includes(w))?2:1);
 return {answer:selected.map(r=>r.body).join('\n\n'),sources:selected.map(r=>({title:r.title,url:r.url}))};
}
