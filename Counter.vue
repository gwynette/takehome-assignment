<template>
  <div>
    <!--Makes sure count doesn't drop below 0-->
    <div v-if="count<0">{{  count = 0  }}</div>
    <div v-else>
    <p>{{  count  }}</p>
    </div>
    <button @click="count++">Increase by 1</button>
    <button @click="count--">Decrease by 1</button>
  </div>
</template>

<script>
export default {
  props: {
    count:{

    }
  }
};

</script>

<style>
</style>