addButton = document.getElementById("addSection");
sectionsDiv = document.getElementById("sections");
const valves = JSON.parse(document.getElementById("valves-data").textContent);

sectionNr=generateSectionNumber();
sectionsDivsArr=[];

addButton.addEventListener("click", function(){addButtonClicked(sectionsDiv)});

function generateSectionNumber(){
    sectionDivs=document.getElementsByName("section-div");

    return sectionDivs.length;
}

function renderDiv(sectionNr, valves){
    sectionDiv = `<div id="section-${sectionNr}" name="section-div">
            <h3>Section ${sectionNr+1}</h3>
            <p>
                <label for="sections-${sectionNr}-name">Section name:</label>
                <input type="text" name="sections[${sectionNr}][name]" id="sections-${sectionNr}-name">
            </p>

            <p>Valves:</p>
            ${valves.map(v=>`
                <input type="checkbox"
                        name="sections[${sectionNr}][valves][]"
                        id="sections-${sectionNr}-valve-${v.gpio}"
                        value="${v.gpio}"
                >
                <label for="sections-${sectionNr}-valve-${v.gpio}">Valve ${v.gpio}</label>
            `).join('')}

            <p>
                <label for="sections-${sectionNr}-duration">Duration (minutes):</label>
                <input type="number" name="sections[${sectionNr}][duration]" id="sections-${sectionNr}-duration">
            </p>
        </div>`
    return sectionDiv;
}

function addButtonClicked(sectionsDiv){
    sectionsDivsArr.push(renderDiv(sectionNr, valves));
    sectionNr++;
    // sectionsDiv.insertAdjacentHTML("afterend", renderDiv(sectionNr, valves));
    sectionsDiv.innerHTML=sectionsDivsArr.join("");
}