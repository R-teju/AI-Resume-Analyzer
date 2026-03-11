async function analyzeResume(){

let resume=document.getElementById("resume").files[0]

let jobdesc=document.getElementById("jobdesc").value

let formData=new FormData()

formData.append("resume",resume)

formData.append("jobdesc",jobdesc)


let response=await fetch("http://127.0.0.1:5000/analyze",{

method:"POST",

body:formData

})


let data=await response.json()

document.getElementById("progress").style.width=data.score+"%"


let strength=""

if(data.score<40){

strength="Weak Resume ❌"

}

else if(data.score<70){

strength="Average Resume ⚠️"

}

else{

strength="Strong Resume ✅"

}


let result = `

<div class="card">
<h3>ATS Score</h3>
<p>${data.score}% - ${strength}</p>
</div>

<div class="card">
<h3>Skill Match</h3>
<p>${data.skill_match}%</p>
</div>

<div class="card">
<h3>Matched Skills</h3>
<p>${data.matched_skills.join(", ")}</p>
</div>

<div class="card">
<h3>Missing Skills</h3>
<p>${data.missing_skills.join(", ")}</p>
</div>

<div class="card">
<h3>Resume Sections</h3>
<p>${data.sections.join(", ")}</p>
</div>

<div class="card">
<h3>Suggestions</h3>
<p>${data.suggestions.join("<br>")}</p>
</div>

`

document.getElementById("output").innerHTML=result

}