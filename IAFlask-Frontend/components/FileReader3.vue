<template>
  <b-container>
    <b-row align-h="center">
      <b-col cols="12" md="8" lg="9" class="text-center">
        <b-img src="@/assets/logo.png" fluid></b-img>
      </b-col>
    </b-row>
    <h1 class="row justify-content-center">
      Algoritmo <small> Cluster Jerarquico</small>
    </h1>
    <b-row class="my-4" align-h="center">
      <b-col cols="3">
        <b-row>
          <b-form-file ref="file" v-model="file" />
          <b-form-input
            v-model="variableEval"
            type="text"
            placeholder="variable de Eval"
          />
          <b-form-input
            v-model="numCluster"
            type="number"
            placeholder="Numero de cluster Jerarquico"
          />
        </b-row>

        <b-row align-v="center">
          <b-button
            :disabled="!file"
            class="mt-2"
            variant="primary"
            block
            @click="readFile"
          >
            Upload
          </b-button>
          <div v-if="error" class="text-danger small ml-2">
            {{ error }}
          </div>
        </b-row>
        <b-row>
          <b-button
            :disabled="!file"
            class="mt-2"
            variant="danger"
            block
            @click="clearData"
          >
            Clear
          </b-button>
        </b-row>
      </b-col>
    </b-row>

    <b-col cols="9">
      <b-table
        v-if="data"
        striped
        hover
        :items="data"
        :busy="loading"
        responsive
      >
        <template #table-busy>
          <div class="text-center text-danger my-2">
            <b-spinner class="align-middle"></b-spinner>
            <strong>Loading...</strong>
          </div>
        </template>
      </b-table>
    </b-col>

    <b-row>
      <b-col cols="12">
        <b-img
          v-if="graphImg"
          :src="graphImg"
          :alt="graphImg"
          class="img-fluid"
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <b-img
          v-if="graphImg3"
          :src="graphImg3"
          :alt="graphImg3"
          class="img-fluid"
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-img
          v-if="graphImg2"
          :src="graphImg2"
          :alt="graphImg2"
          class="img-fluid"
        />
      </b-col>
    </b-row>
    <b-row>
      <b-col cols="12">
        <b-img
          v-if="graphImg4"
          :src="graphImg4"
          :alt="graphImg4"
          class="img-fluid"
        />
      </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  name: 'FileReader3',
  data() {
    return {
      file: null,
      data: [],
      loading: false,
      error: null,
      graphImg: null,
      graphImg2: null,
      graphImg3: null,
      graphImg4: null,
      variableEval: null,
      numCluster: null,
    }
  },
  methods: {
    async readFile() {
      this.loading = true
      this.error = null
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.graphImg4 = null
      try {
        const formData = new FormData()
        formData.append('file', this.$refs.file.files[0])
        formData.append('variableEval', this.variableEval)
        formData.append('numCluster', this.numCluster)

        const response = await this.$axios.$post(
          '/clusterJerarquico',
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
            },
          }
        )
        this.data = JSON.parse(response.data)

        this.graphImg = this.$axios.defaults.baseURL + '/' + response.image
        this.graphImg2 = this.$axios.defaults.baseURL + '/' + response.image2
        this.graphImg3 = this.$axios.defaults.baseURL + '/' + response.image3
        this.graphImg4 =
          this.$axios.defaults.baseURL + '/' + response.imageFinal
      } catch (error) {
        this.error = error.response.data.message
      } finally {
        this.loading = false
      }
    },
    clearData() {
      this.data = []
      this.graphImg = null
      this.graphImg2 = null
      this.graphImg3 = null
      this.graphImg4 = null
      this.file = null
    },
  },
}
</script>

<style></style>
