function running() {
    submit_button.removeEventListener('click', running, true)
    let practice_area = []
    let languages = []
    let honors = []
    let firms = []
    let specialties = []
    let admits = []
    let exports = []
    let sublocations = []
    let locations = []
    let status1 = []
    let status2 = null
    let types = []
    let keyword_type = null
    let keyword_find_with = null
    let keyword_search_string = null
    let min_salary = null
    let max_salary = null
    let cities_locations = []

    let all_practice_area_filters = document.querySelectorAll('.practice_area_filter')
    all_practice_area_filters.forEach((checkbox) => {
        if (checkbox.checked) {
            practice_area.push(checkbox.value)
        }
    })
    let all_languages_filters = document.querySelectorAll('.languages_filter')
    all_languages_filters.forEach((checkbox) => {
        if (checkbox.checked) {
            languages.push(checkbox.value)
        }
    })
    let all_honors_filters = document.querySelectorAll('.honors_filters')
    all_honors_filters.forEach((checkbox) => {
        if (checkbox.checked) {
            honors.push(checkbox.value)
        }
    })
    let all_firms_filters = document.querySelectorAll('.firms_filters')
    all_firms_filters.forEach((checkbox) => {
        if (checkbox.checked) {
            firms.push(checkbox.value)
        }
    })
    let all_specialties_fitlers = document.querySelectorAll('.specialties_filters')
    all_specialties_fitlers.forEach((checkbox) => {
        if (checkbox.checked) {
            specialties.push(checkbox.value)
        }
    })
    let all_admits_filters = document.querySelectorAll('.admits_filters')
    all_admits_filters.forEach((checkbox) => {
        if (checkbox.checked) {
            admits.push(checkbox.value)
        }
    })
    let filter_location_main = document.querySelectorAll('#tabFilterLocations input[name="filter-location-main"]')
    for (let __location of filter_location_main) {
        if (__location.checked) {
            locations.push(__location.value)
        }
    }
    
    let all_exports_filters = document.querySelectorAll('.export_filters')
    all_exports_filters.forEach((checkbox)=>{
        if(checkbox.checked){
            exports.push(checkbox.value)
        }
    })
    
    let sublocation_el = document.querySelectorAll('input[class="filter-location-sub"]')
    for (let __location of sublocation_el) {
        if (__location.checked) {
            sublocations.push(__location.value)
        }
    }
    let types_el = document.querySelectorAll('input[class*="type-filter"]')
    for (let type of types_el) {
        if (type.checked) {
            types.push(type.value)
        }
    }
    let status_el = document.querySelectorAll('input[class*="filter-status"]')
    for (let status of status_el) {
        if (status.checked) {
            status1.push(status.value)
        }
    }
    let status_el2 = document.querySelectorAll('[name="additionalStatus"]')
    for (let status of status_el2) {
        if (status.checked) {
            status2 = status.value
        }
    }
    let keyword_el = document.querySelector('[name="txtKeyword"]')
    if(keyword_el.value){
        keyword_search_string = keyword_el.value
    }
    
    let keyword_type_filters_el = document.querySelectorAll('input[name="lbKeyWordType"]')
    keyword_type_filters_el.forEach((checkbox)=>{
        if(checkbox.checked){
            keyword_type = checkbox.value
        }
    })
    
    let keyword_find_with_el = document.querySelectorAll('input[name="lbKeyWordSearchWith"]')
    keyword_find_with_el.forEach((checkbox)=>{
        if(checkbox.checked){
            keyword_find_with = checkbox.value
        }
    })
    
    let cities_locations_el = document.querySelectorAll('input[name="cities-locations"]')
    cities_locations_el.forEach((checkbox)=>{
        if(checkbox.checked){
            cities_locations.push(checkbox.value)
        }
    })
    
    let min_salary_el = document.querySelector('#txtMinSalary')
    if(min_salary_el.value){
        min_salary = min_salary_el.value
    }
    
    let max_salary_el = document.querySelector('#txtMaxSalary')
    if(max_salary_el.value){
        max_salary = max_salary_el.value
    }
    eel.run_main(locations, sublocations, cities_locations, practice_area, keyword_search_string, keyword_type, keyword_find_with, firms, languages, honors, types, specialties, admits, status1, status2, min_salary, max_salary, exports)
    window.close()
    // submit_button.addEventListener('click', running, true)
}
const submit_button = document.querySelector('#btnSubmit')
submit_button.addEventListener('click', running, true);


(() => {
    let filter_location_main = document.querySelectorAll('#tabFilterLocations input[name="filter-location-main"]')
    let main_locations = []
    for (let _location of filter_location_main) {
        _location.onclick = () => {
            let sublocations = []
            for (let __location of filter_location_main) {
                if(__location.checked) {
                    if(!main_locations.includes(__location.value)){
                        main_locations.push(__location.value)
                    }
                    sublocations.push(...Object.keys(SUBCATEGORIES['locations'][__location.value.toLowerCase()]))
                }else{
                    if(main_locations.includes(__location.value)){
                        main_locations.shift(main_locations.indexOf(__location));
                    }
                }
                let sub_locations_el = document.querySelector("#sub-locations-list")
                let sublocations_html = ""
                for (let _location of sublocations) {
                    sublocations_html += `<li class="filter-location-sub"><div class="k-top"><input name="sub-locations" class="filter-location-sub" value="${_location}" type="checkbox"/><span style="padding-left:5px"></span>${_location}</div></li><ul id="${_location.replace(" ","-").toLowerCase()}-cities-list" class="k-group" role="group" style="display: block; overflow: visible; height: auto;"></ul>`
                }
                sub_locations_el.innerHTML = ""
                sub_locations_el.innerHTML = sublocations_html
            }
            let all_sublocations = document.querySelectorAll('input[name="sub-locations"]')
            for(let _state of all_sublocations){
                _state.onclick = () => {
                    ul_tag_id = _state.value.replace(" ","-")
                    let all_cities_under_state = []
                    if(_state.checked){
                        for(let ___location of main_locations){
                            try{
                                all_cities_under_state.push(...SUBCATEGORIES['locations'][___location.toLowerCase()][_state.value])
                                console.log(...SUBCATEGORIES['locations'][___location.toLowerCase()][_state.value])
                            }catch(err){
                                // pass
                            }
                        }
                    }
                    let cities_el = document.querySelector(`#${ul_tag_id.toLowerCase()}-cities-list`)
                    let cities_html = ""
                    for(let city of all_cities_under_state){
                        city_value = city.replace(" ","-")
                        cities_html += `<li
                        role="treeitem"
                        class="k-item k-last"
                        aria-checked="true"
                        aria-selected="false"
                        aria-expanded="false"
                        data-expanded="false"
                        >
                        <div class="k-bot">
                            <span class="k-checkbox-wrapper" role="presentation"
                            ><input name="cities-locations"
                                type="checkbox" value=${city_value}></span
                            ><span class="k-in">${city}</span>
                        </div>
                        </li>`
                    }
                    cities_el.innerHTML = ""
                    cities_el.innerHTML = cities_html
                }
            }
        }
    }
})()