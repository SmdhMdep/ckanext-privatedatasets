/*
 * (C) Copyright 2014 CoNWeT Lab., Universidad Politécnica de Madrid
 *
 * This file is part of CKAN Private Dataset Extension.
 *
 * CKAN Private Dataset Extension is free software: you can redistribute it and/or
 * modify it under the terms of the GNU Affero General Public License as
 * published by the Free Software Foundation, either version 3 of the
 * License, or (at your option) any later version.
 *
 * CKAN Private Dataset Extension is distributed in the hope that it will be useful, but
 * WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
 * or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
 * License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with CKAN Private Dataset Extension. If not, see
 * <http://www.gnu.org/licenses/>.
 *
 */

/* Dataset allowed_users, searchable and acquire_url toggler
 * allowed_users, acquire_url and searchable can only be active when a 
 * user attempts to create a private dataset
 */

window.onload = function() {
  this.original_acquire_url = $('[name=acquire_url]').val();
  this.mySelect.onchange(); //Initial
}

var mySelect = document.getElementById('field-visibility');
mySelect.onchange = (event) => {
  var e = document.getElementById("field-visibility");
  var d = document.getElementById("hide-me");
  var ds_private = e.options[e.selectedIndex].text;

  console.log(ds_private);

  if (ds_private == 'Private User Shareable') {
    $('#field-allowed_users_str').prop('disabled', false);      //Enable
    $('#hide-me').show();
  } else {
    //$('#field-allowed_users_str').prop('disabled', true);       //Disable
    //Remove previous values
    $('#field-allowed_users_str').select2('val', '');

    //Remove previous values
    $('#hide-me').hide();
  }
}
