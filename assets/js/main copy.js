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
login_btn.addEventListener("click", function(){
    login_form.classList.add("opacity")
    login_form.classList.toggle("show")
    setTimeout(function(){
        login_form.classList.remove("opacity")
    }, 1000)
})

close_login_form.addEventListener("click", function(){
    login_form.classList.add("opacity")
    //debugger
    setTimeout(function(){
        login_form.classList.toggle("show")
        login_form.classList.remove("opacity")
    }, 1000)
})

/* ================= SWITCH LOGIN AND REGISTER ================= */
register_btn = document.querySelector(".register_btn")
login_btn = document.querySelector(".login_btn")
login_on_register_btn = document.querySelector(".login_on_register_btn")
login_form_div = document.querySelector("#login_form")
register_form_div = document.querySelector("#register_form")
register_btn.addEventListener("click", function(e){
    //debugger
    e.preventDefault()
    login_form_div.classList.add("opacity")
    setTimeout(function(){
        login_form_div.classList.add("hidden_element")
        register_form_div.classList.remove("hidden_element")
    }, 1000)

    setTimeout(() => {
        register_form_div.classList.remove("opacity")
    }, 1200);

})

login_on_register_btn.addEventListener("click", function(e){
    //debugger
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