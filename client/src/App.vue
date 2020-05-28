<template>
  <v-app>
    <!-- Sizes your content based upon application components -->
    <v-content style="padding: 0px">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      schedules: [],
      icons: [
        {
          icon: 'fab fa-github',
          url: 'https://github.com/jojo20872/MC-Schedule-Builder',
        },
        {
          icon: 'fab fa-linkedin',
          url: 'https://www.linkedin.com/in/jschne/',
        },
      ],
      menuItems: [
        { title: 'Home', path: '/home', icon: 'fas fa-home' },
        { title: 'Create', path: '/builder', icon: 'fas fa-plus-square' },
        { title: 'Sign In', path: '/signin', icon: 'fas fa-sign-in-alt' },
      ],
    };
  },
  methods: {
    getSchedules() {
      const path = 'http://localhost:5000/schedules';
      axios
        .get(path)
        .then((res) => {
          this.schedules = res.data.schedules;
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
          this.getSchedules();
        });
    },
    createSchedule() {

    },
  },
  created() {
    this.getSchedules();
  },
};
</script>

<style>
/* @import url('https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap'); */

html,
body,
#app {
  height: 100%;
}

.v-footer--fixed {
  position: relative;
}

.v-toolbar__content, .v-toolbar__extension {
  padding: 0px
}
</style>
