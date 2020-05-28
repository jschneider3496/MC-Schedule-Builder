import Vue from 'vue';
import Router from 'vue-router';
import Ping from './components/Ping.vue';
import Builder from './components/Builder.vue';
import Home from './components/Home.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/ping',
      name: 'Ping',
      component: Ping,
    },
    {
      path: '/builder/:id',
      name: 'Builder',
      component: Builder,
    },
    {
      path: '/',
      name: 'Home',
      component: Home,
    },

  ],
});
