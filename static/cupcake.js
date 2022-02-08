"use strict";

const CUPCAKE_URL = "http://localhost:5001/api";

let CUPCAKES_LIST = "";

async function getCupcakes(){
    console.debug("getCupcakes")

    const url = CUPCAKE_URL + "/cupcakes";
    console.log(url);
    const response = await axios.get(url);

    displayCupcakes(response.data.cupcakes)

    CUPCAKES_LIST = response.data.cupcakes;
}

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


getCupcakes();