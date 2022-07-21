/*===== EXPANDER MENU =====*/
const showMenu = (toggleId, navbarId, bodyId)=>{
    const toggle = document.getElementById(toggleId),
    navbar = document.getElementById(navbarId),
    bodypadding = document.getElementById(bodyId)

    if(toggle, navbar){
        toggle.addEventListener('click', ()=>{
            navbar.classList.toggle('expender')
            bodypadding.classList.toggle('body-pd')
        })
    }
}
showMenu('nav-toggle', 'navbar', 'body-pd')
/*===== LINK ACTIVE =====*/
const linkColor = document.querySelectorAll('.nav__link');
function colorLink(){
    linkColor.forEach(l=>l.classList.remove('active'))
    this.classList.add('active')
}
linkColor.forEach(L=> L.addEventListener('click', colorLink))

/*===== COLLAPSE MENU =====*/
const linkCollapse = document.getElementsByClassName('collapse__link')
var i 
for (i = 0; i < linkCollapse.length; i++) {
    linkCollapse[i].addEventListener('click', function(){
        const collapseMenu = this.nextElementSibling
        collapseMenu.classList.toggle('showCollapse')

        const rotate = collapseMenu.previousElementSibling
        rotate.classList.toggle('rotate')
    })
}

/*================== FORM ==================*/
login_btn = document.querySelector(".login_btn")
login_form = document.querySelector(".login_form")
close_login_form = document.querySelector(".close_login_form")

toggle_form = function(log_form){
    log_form.classList.add("opacity")
    log_form.classList.toggle("show")
    if(log_form.classList.contains("show")){
        document.querySelector('#email_username').focus()
    }
    setTimeout(function(){
        log_form.classList.remove("opacity")
    }, 1000)
}

show_for = function(btn, log_form){
    if(btn && log_form){
        btn.addEventListener("click", function(){
            toggle_form(log_form)
        })
    }
}


show_for(login_btn, login_form)
show_for(close_login_form, login_form)

/* ================= SWITCH LOGIN AND REGISTER ================= */
register_btn = document.querySelector(".register_btn")
login_btn = document.querySelector(".login_btn")
login_on_register_btn = document.querySelector(".login_on_register_btn")
login_form_div = document.querySelector("#login_form")

register_form_div = document.querySelector("#register_form")

if (register_btn && login_form_div && register_form_div) {
    register_btn.addEventListener("click", function(e){
        e.preventDefault()
        login_form_div.classList.add("opacity")
        setTimeout(function(){
            login_form_div.classList.add("hidden_element")
            register_form_div.classList.remove("hidden_element")
        }, 800)

        setTimeout(() => {
            register_form_div.classList.remove("opacity")
        }, 1000);

    })
}
if(login_on_register_btn && register_form_div && login_form_div){
    login_on_register_btn.addEventListener("click", function(e){
        e.preventDefault()
        register_form_div.classList.add("opacity")
        setTimeout(function(){
            register_form_div.classList.add("hidden_element")
            login_form_div.classList.remove("hidden_element")
        }, 1000)

        setTimeout(() => {
            login_form_div.classList.remove("opacity")
        }, 1200);

    })
}

/********************************Request function ************************************/
sendReq = function(req_url, form = null, queryMethod='POST'){
    var HttpRequest = new XMLHttpRequest();
    var token_input = document.querySelector('input[name="csrfmiddlewaretoken"]') 
    HttpRequest.open(queryMethod, req_url, true);
    HttpRequest.setRequestHeader("X-CSRFToken", token_input.value)
    if(form != null){
        var data = new FormData(form);
        HttpRequest.send(data);
    }else{
        HttpRequest.send(data);
    }
    return HttpRequest
}
/********************************AJOUT DE CATEGORIE POPULAIRE ET SURGESTION************************************/
var cat_url = document.getElementById('get_popular_category')
var cat_surg_url = document.getElementById('get_surgestion_category')
var sujet_url = document.getElementById('get_sujet')
var subject_div = document.querySelector('.subject_div')
var populare_div = document.querySelector('.populare_div')
var surgestion_div = document.querySelector('#categoryList')
if(sujet_url && subject_div){
    var req_suj = sendReq(sujet_url.href, null, 'GET')
    req_suj.onreadystatechange = function() {
            if (req_suj.readyState === 4) {
            response = req_suj.response
            if(req_suj.status === 200){
                subject_div.innerHTML = response
            }else(
                alert(response.message)
            )
            }
    }
}
if(cat_url && populare_div){
    var req = sendReq(cat_url.href, null, 'GET')
    req.onreadystatechange = function() {
            if (req.readyState === 4) {
            response = req.response
            if(req.status === 200){
                populare_div.innerHTML = response
            }else(
                alert(response.message)
            )
            }
    }
}
if(cat_surg_url && surgestion_div){
    var req_surg = sendReq(cat_surg_url.href, null, 'GET')
    req_surg.onreadystatechange = function() {
            if (req_surg.readyState === 4) {
            response_surg = req_surg.response
            if(req_surg.status === 200){
                surgestion_div.innerHTML = response_surg
            }else(
                alert(response_surg.message)
            )
            }
    }
}

/*
 *                   GESTION DE LA CONNECTION ET L'ENREGISTREMENT
*/
var login_url = document.getElementById('login_url_id') 
var register_url = document.getElementById('signup_url_id')
var register_form_element = document.querySelector("#register_form_element");
var login_form_element = document.querySelector("#login_form_element");
var input = document.querySelector("#login_btn")
/* *************************** Soumition du formulaire de connection **************************** */
if (login_url && login_form_element) {
    login_form_element.addEventListener('submit', function(e) {
        e.preventDefault()
        req = sendReq(login_url.href, login_form_element)
        req.onreadystatechange = function() {
             if (req.readyState === 4) {
                response = JSON.parse(req.response)
                if(req.status === 200 && response.is_connect === true){
                    window.location.replace(window.location.href.replace("#",""))
                }else(
                    alert(response.message)
                )
             }
        }
        
    })
}
/* *************************** Soumition du formulaire d'inscription **************************** */
if (register_form_element && register_url) {
    register_form_element.addEventListener('submit', function(e) {
        e.preventDefault()
        req = sendReq(register_url.href, register_form_element)
        if(req.status === 200){
            window.location.replace(window.location.href.replace("#",""))
        }
    })
}


/**
 * ******************************************  SE DECONNECTER ***********************************************
 */
log_out_btn = document.getElementById('log_out_btn')
if (log_out_btn) {
    log_out_btn.addEventListener('click', function(e){
        e.preventDefault()
        if(confirm("Voulez-vous vous deconnecter de la page ?")){
            req = sendReq(log_out_btn.href, null, "GET")
            req.onreadystatechange = function() {
                if (req.readyState === 4) {
                    response = JSON.parse(req.response)
                    if(req.status === 200 && response.is_connect === false){
                        window.location.replace(window.location.href.replace("#",""))
                    }else(
                        alert(response.message)
                    )
                }
            }
        }
    })
}

/**
 * ****************************Visualisation image***********************************
 */
 var image = document.querySelector('.commentaire_img')

 var previewPicture = function(e){
     const[picture] = e.files   
     if(picture){
         image.src = URL.createObjectURL(picture)
     }
     var textarea = document.querySelector('#comment-text-area')
     textarea.removeAttribute('required')
 }

//************************************ GESTION DES AVIS **************************************//
like_btn = document.querySelectorAll('.pouces')
dislike_btn = document.querySelectorAll('.dislike')

like_btn.forEach((like)=>{
    like.addEventListener('click', function(e){
        e.preventDefault()
        pouce = this
        dislike = this.parentElement.querySelector('.dislike')
        comment = this.parentElement.querySelector('.commentaires')
        unnotice = this.parentElement.querySelector('.unnotice')
        if (pouce.classList.contains('is_active')) {
            req = sendReq(unnotice.href, null, "GET")
        }else{
            req = sendReq(pouce.href, null, "GET")
        }
        req.onreadystatechange = function(){
            if (req.readyState === 4) {
                response = JSON.parse(req.response)
                if(req.status === 200 && response.request_is_done === true){
                    pouce.classList.toggle('is_active')
                    if (dislike.classList.contains('is_active')) {
                        dislike.classList.remove('is_active')
                    }
                    dislike.innerText = response.dislike_nber
                    pouce.innerText = response.like_nber
                    comment.innerText = response.respons_number
                }else{
                    if (response.is_connect === false) {
                        toggle_form(login_form)
                    }
                }
            }
        }
    })
})

dislike_btn.forEach((dislike)=>{
    dislike.addEventListener('click', function(e){
        e.preventDefault()
        dislike = this
        like = this.parentElement.querySelector('.pouces')
        comment = this.parentElement.querySelector('.commentaires')
        unnotice = this.parentElement.querySelector('.unnotice')
        if (dislike.classList.contains('is_active')) {
            req = sendReq(unnotice.href, null, "GET")
        }else{
            req = sendReq(dislike.href, null, "GET")
        }
        req = sendReq(this.href, null, "GET")
        req.onreadystatechange = function(){
            if (req.readyState === 4) {
                response = JSON.parse(req.response)
                if(req.status === 200 && response.request_is_done === true){
                    dislike.classList.toggle('is_active')
                    if (like.classList.contains('is_active')) {
                        like.classList.remove('is_active')
                    }
                    dislike.innerText = response.dislike_nber
                    like.innerText = response.like_nber
                    comment.innerText = response.respons_number
                }else{
                    if (response.is_connect === false) {
                        toggle_form(login_form)
                    }
                }
            }
        }
    })
})

/**================================================================**/
formulaire = document.querySelector('.commentaire_form')
log_out_btn = document.querySelector('#log_out_btn')

if(log_out_btn && formulaire){
    comment_url = document.querySelector('.commentaire_form').action
    send_btn = document.querySelector('.send_btn')
    formulaire.addEventListener('submit', function(e){
        e.preventDefault()
        req = sendReq(comment_url, formulaire)
        req.onreadystatechange = function() {
            if (req.readyState === 4){
                response = JSON.parse(req.response)
                if(req.status === 200 && response.is_connect === true){
                    window.location.replace(window.location.href.replace("#",""))
                }else(
                    alert("Une erreur s'est produite veuillez reessayer plus tard !")
                )
            }
        }
    })
}else{
    if(formulaire){
        formulaire.addEventListener('click', function(e){
            e.preventDefault()
            toggle_form(login_form)
        })
    }
}

/*
                        GESTION DES ONGLETS DU MENU
 */
var nav_list = document.querySelector('.navigation')
var links = nav_list.querySelectorAll('a')
var link_exist = false
links.forEach(function(l) {
    l.classList.remove('active')
    if(document.location.pathname.includes(l.id)){
        l.classList.add('active')
        link_exist = true
    }
})

if(!link_exist){
    document.querySelector('#home').classList.add('active')
}