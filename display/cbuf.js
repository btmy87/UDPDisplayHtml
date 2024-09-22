// javascript class implementing a circular buffer

class CBuf {
  constructor(arrayLength, init_val=NaN) {
    this.data = new Float64Array(arrayLength).fill(init_val);
    this.length = arrayLength;
    this.index = 0; // next index to set
    this.init_val = init_val;
  }
  add_val(newVal) {
    // add a single value t the buffer
    this.data[this.index] = newVal;
    this.index = (this.index + 1) % this.length;

    // put nan flag in next value
    let nextIndex = (this.index + 1) % this.length;
    this.data[nextIndex] = this.init_val;
  }
}