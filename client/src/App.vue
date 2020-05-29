<template>
  <v-app>
    <!-- Sizes your content based upon application components -->
    <v-content style="padding: 0px">
      <router-view></router-view>
    </v-content>
  </v-app>
</template>

<style>
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
