"use strict";

const CUPCAKE_URL = "http://localhost:5000/api";

let CUPCAKES_LIST = "";

/** Gets cupcakes JSON from server and calls displayCupcakes */
async function getCupcakes(){
    console.debug("getCupcakes")

    const url = CUPCAKE_URL + "/cupcakes";
    console.log(url);
    const response = await axios.get(url);

    displayCupcakes(response.data.cupcakes)

    CUPCAKES_LIST = response.data.cupcakes;
}

/** Renders cupcakes from cupcakes JSON */
function displayCupcakes(cupcakes){
    console.debug("displayCupcakes")

    const $cupcakeList = $("#cupcake-list");

    for(let cupcake of cupcakes){
        $cupcakeList.append(
            $(`<li>
                <img src = ${cupcake.image}>
                <p>Flavor: ${cupcake.flavor}</p>
                <p>Rating: ${cupcake.rating}</p>
                <p>Size: ${cupcake.size}</p>
            </li>`
            )
        )
    }
}

/** Handles cupcake form submissions and adds to server database */
async function addCupcake(evt){
    evt.preventDefault();

    const flavor = $("#flavor").val();
    const size = $("#size").val();
    const rating = $("#rating").val();
    const imgURL = $("#imgURL").val();

    const response = await axios.post(CUPCAKE_URL + "/cupcakes",
    {flavor:flavor, size:size, rating:rating, image:imgURL});
    
    addCupcakeHTML(response);
}

/** Appends newly added cupcake to DOM list */
function addCupcakeHTML(response){
    const cupcake = response.data.cupcake;

    $("#cupcake-list").append($(
        `<li>
        <img src = ${cupcake.image}>
        <p>Flavor: ${cupcake.flavor}</p>
        <p>Rating: ${cupcake.rating}</p>
        <p>Size: ${cupcake.size}</p>
        </li>`
    ))
}

$("#cupcake-submit").on("click", addCupcake)

getCupcakes();