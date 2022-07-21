/*
Je recupere toute les textes ou je pourrais ajoupter le span de spoiler.
je dois compter le nombre de ligne du texte 
ajouter le spoile pour les n premieres lignes
 */





/*
LORSQUE je clique sur le boutton dans la class .spoiler 
ALORS
    j'ajoute la classe .visible à l'élement suivant


var button = document.querySelector('.spoiler button');
button.addEventListener('click', function() {
    this.nextElementSibling.classList.add('visible');
    this.parentNode.removeChild(this);
})
*/

var elements = document.querySelectorAll('.spoiler');

var createSpoilerButton = function(element) {
    //On crée le span
    var span = document.createElement('span');
    span.className = 'spoiler-content';
    span.innerHTML = element.innerHTML;

    //On crée le bouton 
    var button = document.createElement('button');
    button.textContent = 'Lire la suite';

    //On ajoute les element à la DOM
    element.innerHTML = '';
    element.appendChild(button);
    element.appendChild(span);

    // On met les ecouteurs d'evenement
    button.addEventListener('click', function() {
        button.parentNode.removeChild(button);
        span.classList.add('visible');
    })
};
for (var i = 0; i < elements.length; i++) {
    createSpoilerButton(elements[i]);
}