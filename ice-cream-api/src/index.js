
search_ice_cream()

const box = document.getElementById('box')

fetch('http://127.0.0.1:5000/flavors')
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    }
    return response.json();
  })
  .then(data => {
    data.forEach(flavor => {
        box.innerHTML += string(flavor)  
    })
    
  })
  .catch(error => {
    console.error('There was a problem with the fetch operation:', error);
  })
  .finally(() => {
    search_ice_cream()
  })

function string(flavor) {
    return `<div class='flavorlist'>

        <h3>${flavor.flavor}</h3>
        <h3 style="white-space: nowrap;">${flavor.flavor} ${(flavor.image)} ${render_stars(flavor.rating)}</h3>
    </div>`;

}

function render_stars (rating) {
    let stars = ""
    for (let i = 1; i <= rating; i++) {
        stars += "\u2B50"
    }
    return stars
} 

function search_ice_cream() {

    let input = document.getElementById('searchbar').value
    input = input.toLowerCase();
    let x = document.getElementsByClassName('ice_cream');
    for (i = 0; i < x.length; i++) {
        if (!x[i].innerHTML.toLowerCase().includes(input) || input.length === 0) {
            x[i].style.display = "none";
        }
        else {
            x[i].style.display = "list-item";
        }
    }
}
