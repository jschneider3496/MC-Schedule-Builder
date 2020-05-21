<template>
  <div class="container">
    <div class="row">
      <div class="col-sm-10">
        <h1>{{name}}</h1>
        <hr />
        <br />
        <br />

        <mdb-dropdown multiLevel>
          <mdb-dropdown-toggle slot="toggle" color="mdb-color">Click me</mdb-dropdown-toggle>
          <mdb-dropdown-menu>
            <mdb-dropdown-item tag="div" class="p-0" submenu>
              <mdb-dropdown class="w-100">
                <mdb-dropdown-item slot="toggle" submenuIcon="caret-right">Click me</mdb-dropdown-item>
                <mdb-dropdown-menu class="ml-2 rounded-0 border-0 z-depth-1">
                  <mdb-dropdown-item href="#">Item 1</mdb-dropdown-item>
                  <mdb-dropdown-item href="#">Item 2</mdb-dropdown-item>
                  <mdb-dropdown-item href="#">Item 3</mdb-dropdown-item>
                </mdb-dropdown-menu>
              </mdb-dropdown>
            </mdb-dropdown-item>
            <mdb-dropdown-item class="p-0" submenu>
              <mdb-dropdown class="w-100">
                <mdb-dropdown-item slot="toggle" submenuIcon="caret-right">Click me</mdb-dropdown-item>
                <mdb-dropdown-menu class="ml-2 rounded-0 border-0 z-depth-1">
                  <mdb-dropdown-item href="#">Item 1</mdb-dropdown-item>
                  <mdb-dropdown-item href="#">Item 2</mdb-dropdown-item>
                  <mdb-dropdown-item href="#">Item 3</mdb-dropdown-item>
                </mdb-dropdown-menu>
              </mdb-dropdown>
            </mdb-dropdown-item>
          </mdb-dropdown-menu>
        </mdb-dropdown>


        <br />
        <br />
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">CRN</th>
              <th scope="col">Course</th>
              <th scope="col">Days</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(c, index) in schedule" :key="index">
              <td>{{ c.crn }}</td>
              <td>{{ c.title }}</td>
              <td>{{ c.days }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Update</button>
                  <button type="button" class="btn btn-danger btn-sm">Delete</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {
  mdbDropdown,
  mdbDropdownToggle,
  mdbDropdownMenu,
  mdbDropdownItem,
} from 'mdbvue';

export default {
  name: 'DropdownPage',
  components: {
    mdbDropdown,
    mdbDropdownToggle,
    mdbDropdownMenu,
    mdbDropdownItem,
  },
  data() {
    return {
      schedule: [],
      name: '',
      id: '',
    };
  },
  methods: {
    getSchedule() {
      const path = 'http://localhost:5000/builder';
      axios
        .get(path)
        .then((res) => {
          this.schedule = res.data.schedule;
          this.name = res.data.name;
          this.id = res.data.id;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
  },
  created() {
    this.getSchedule();
  },
};
</script>
