import '@fortawesome/fontawesome-free/css/all.min.css';
import 'bootstrap-css-only/css/bootstrap.min.css';
import 'mdbvue/lib/css/mdb.min.css';
import 'bootstrap/dist/css/bootstrap.css';
import BootstrapVue from 'bootstrap-vue';
import Vue from 'vue';
import vSelect from 'vue-select';
import Vuetify from 'vuetify';
import App from './App.vue';
import router from './router';
import 'vue-select/dist/vue-select.css';
import 'vuetify/dist/vuetify.min.css';
import 'font-awesome/css/font-awesome.min.css';

Vue.component('v-select', vSelect);


Vue.use(BootstrapVue);
Vue.use(Vuetify);
Vue.config.productionTip = false;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app');
