import Vue from 'vue'
import VueRouter from 'vue-router';
import axios from 'axios';

/* this is creating all router paths. When a user lands on the path
vue router will load component(this corresponds with the file names 
  in "view" folder). Props are just data we want to pass to the 
  html. Note that these props aren't really used too often */
const routerOptions = [
  { path: '/', 
    component: 'home', 
    props: {
      title: 'Home Page',
      },
    },
]
/* this variable actually maps the 
route to the component in the views folder*/
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/views/${route.component}.vue`)
  }
})
Vue.use(VueRouter)

/* this creates an instance 
of vuerouter and exports it. 
This is used in the navBar.vue 
file in the component folder*/ 
const router = new VueRouter({
  routes,
  mode: 'history'
})
export default router




