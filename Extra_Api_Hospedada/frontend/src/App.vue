<template>
  <div id="app">
    <OperadorasList />
  </div>
</template>

<script>
import OperadorasList from './components/OperadorasList.vue';

export default {
  name: 'App',
  components: {
    OperadorasList,
  },
};
</script>

<style>
#app {
  font-family: 'Arial', sans-serif;
  text-align: center;
  margin-top: 20px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 20px;
}
</style>
