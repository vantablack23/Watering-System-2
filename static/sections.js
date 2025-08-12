addButton = document.getElementById("addSection");
sectionsDiv = document.getElementById("sections");
const valves = JSON.parse(document.getElementById("valves-data").textContent);

sectionNr=generateSectionNumber();
sectionsDivsArr=[];

addButton.addEventListener("click", function(){addButtonClicked(sectionsDiv)});

document.getElementsByName("deleteSection").forEach(element => {
    element.addEventListener("click", deleteButtonClicked);
}); 

function generateSectionNumber(){
    sectionDivs=document.getElementsByName("section-div");

    return sectionDivs.length;
}

function renderDiv(sectionNr, valves){
    sectionDiv = `<div id="section-${sectionNr}" name="section-div">
            <hr>
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
            <button type="button" name="deleteSection" id="delete-section-${sectionNr}">Delete</button>
        </div>`
    return sectionDiv;
}

function addButtonClicked(sectionsDiv){
    sectionsDiv.insertAdjacentHTML("afterend", renderDiv(sectionNr, valves));
    sectionNr++;

    document.getElementsByName("deleteSection").forEach(element => {
        element.addEventListener("click", deleteButtonClicked);
    }); 
}

function deleteButtonClicked(){
    document.getElementById("section-"+this.id.slice(15)).remove();
}